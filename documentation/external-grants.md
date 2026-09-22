# External permissions for modules

The core now separates external **identity connections** from **consumer-bound
permissions (grants)**. An identity permits Google panel login. A grant permits a
specific module to use a reviewed provider capability while its owner is offline.

The initial provider is Google. Registered consumers/capabilities are:

| Consumer | Capability | Google scope |
| --- | --- | --- |
| `cloud-sync` | `google-drive` | `https://www.googleapis.com/auth/drive` |
| `cloud-sync` | `google-drive-readonly` | `https://www.googleapis.com/auth/drive.readonly` |

Full Drive access is needed to synchronize arbitrary existing files/folders,
including edits and deletions. Read-only access is available for download-only
implementations. The NAS must request additional consent; linking alone never
grants either capability. Enable Drive API in the Google project before actual
Drive use. External Testing grants that request Drive are subject to Google's
seven-day refresh-token expiry and test-user requirements; plan production and
verification before claiming unattended long-term synchronization.

See [Google's Drive scopes](https://developers.google.com/workspace/drive/api/guides/api-specific-auth)
and [offline authorization](https://developers.google.com/identity/protocols/oauth2/web-server#offline).

## Ownership and extensibility

A grant is bound to `connectionId`, `consumer`, `capability`, provider scope,
Linux owner/principal, account epoch, provider settings revision and module
installation identity. Tokens are encrypted with the existing core key;
associated data binds ciphertext to its grant and authorization context.

The contract is not specific to Cloud Sync. To add another consumer such as
Files, add its reviewed capabilities in `backend/internal/api/grant_policy.go`.
It gets separate grants, consent and revocation. The server derives scopes from
that policy; browser code and module manifests cannot introduce arbitrary OAuth
scopes, token endpoints or consumer privileges. Another provider needs its own
OAuth adapter and consent UI; the grant storage/broker model remains reusable.

Google account linking settings and secrets remain NAS-wide. Drive access and
refresh tokens never appear in browser APIs. Provider refresh happens in core.
Only a short-lived access token is delivered to the authorized module backend.

## Browser contract

Use the existing same-origin `@panasms/client` request function. These requests
use the panel session, CSRF protections and an HttpOnly authorization-flow cookie.
The current user can manage only their own connections and grants.

1. `GET /api/v1/external/connections`: select an owned Google identity.
2. `GET /api/v1/external/grants`: list metadata, including `id`, `connectionId`,
   `consumer`, `capability`, `scope`, `status`, `created`. No tokens or secrets.
3. Start new consent:

```json
{
  "purpose": "grant",
  "connectionId": "<selected-connection-id>",
  "consumer": "cloud-sync",
  "capability": "google-drive",
  "password": "<current-NAS-password>"
}
```

POST this to `/api/v1/external/google/start`. It returns `url` and `expiresIn`.
Open the URL in a separate tab. The request uses offline consent, PKCE, nonce and
a subject login hint. Core verifies the returned Google subject matches the
selected identity; the hint alone is not trusted.

4. POST `{}` to `/api/v1/external/google/poll` every 3–4 seconds in the original
   browser. `202 {"status":"pending"}` means keep waiting.
   Success is `200 {"status":"granted","grantId":"..."}`. No credentials are
   returned. Store the resulting grant ID in the module account/job configuration.
5. POST `{}` to `/api/v1/external/google/cancel` to abandon an attempt.
6. DELETE `/api/v1/external/grants` with `{"id":"...","password":"..."}` to
   revoke an owned permission. The profile Connections page also exposes revocation.

Reauthorizing the same connection/consumer/capability replaces its previous grant
with a **new ID**. Update the module's reference only after successful consent.
An unsuccessful or cancelled attempt does not overwrite the working grant.
Expiry, restart or settings changes require a fresh flow. One browser has one
pending external authorization attempt; starting another cancels the first.

### Shared consent component

The host exports `PaNasMsSDK.external.GoogleConnect`, with declarations in
`module-sdk/types/external.d.ts`. Add `external` to your Vite externals mapping
(`@panasms/external` → `PaNasMsSDK.external`) and corresponding TypeScript path.

```tsx
import { GoogleConnect } from '@panasms/external'

<GoogleConnect
  grant={{ connectionId, consumer: 'cloud-sync', capability: 'google-drive' }}
  onComplete={(grantId) => {
    if (grantId) saveModuleConnection({ connectionId, grantId })
  }}
/>
```

The component handles password proof, explicit permission description, consent
tab, polling, cancellation and localized errors. Mount it with a stable selected
connection and callback while a flow is active. Do not implement a second copy
of the core client-secret form or exchange Google codes in the module.
Feature-detect `PaNasMsSDK.external` when supporting earlier core builds; the
prototype version string alone does not distinguish this development update.

## Module backend contract

The private broker listens at `/run/panasms-core/grants.sock`. It is **not**
registered on the public HTTP router. Directory mode is 0700 and socket mode 0600,
owned by the core service user. Root is also permitted for existing module units.

The broker obtains PID/UID via Unix `SO_PEERCRED` and identifies the consumer
from the peer's systemd cgroup v2:
`/system.slice/panasms-module-<consumer>.service` (including child cgroups).
No module-ID header, browser cookie or supplied consumer string authenticates a
caller. It verifies the consumer is enabled and registered on every request.
Non-systemd/cgroup-v1 callers fail closed. Call from the module's **main service**,
not a separately named per-user transient unit or an interactive shell.

```go
import "github.com/PaNasMs/module-sdk/external"

broker := external.New()
access, err := broker.Token(ctx, job.GrantID, job.Owner)
// access.AccessToken, access.TokenType, access.ExpiresAt, access.Scope
// Never return this object to browser code or log it.
```

The wire request is `POST /v1/token`:

```json
{"grantId":"<grant-id>","owner":"<Linux-job-owner>"}
```

The response contains `accessToken`, `tokenType` (`Bearer`), `expiresAt` (RFC3339),
and `scope`. It contains **no refresh token, client secret or client ID**.
Derive `job.Owner` from authenticated task creation, not arbitrary public request
fields. A shared module service is responsible for isolating its users' jobs and
not exposing one user's permission to another user.

Core serializes grant operations and refresh, preserves refresh-token rotation,
persists renewed tokens before responding and rechecks dynamic module/account
authorization after refresh. Calls while the token is still valid reuse it.
The endpoint checks permissions without scanning local data disks.

| Response | Module behavior |
| --- | --- |
| 200 | Use the token only for this grant and within its returned expiry/scope. |
| 403 | Permission, owner or module is unavailable. Stop using cached credentials and pause affected jobs. |
| 409, `external.reconnectRequired` | Ask the owner to authorize again. Do not silently fall back to a module-owned token. |
| 503 | Temporary refresh/core failure. Back off; preserve task progress. Do not convert a transient failure into permanent grant revocation. |

The Go SDK preserves HTTP status and error code via `*external.Error`.

### Integrating rclone

The old Cloud Sync `account_import` contract expects access/refresh tokens and
optional client credentials. It **must change** for core grants. Keep only the
grant reference in persistent module configuration. Ask the broker for access
when a task starts and before token expiry; periodically recheck authorization
(for example every 30 seconds while transferring) so local revocations stop jobs.

Feed only the temporary token into a private runtime rclone configuration, never
command-line arguments, browser responses or logs. Implement token replacement
for running transfers or pause/resume at a safe checkpoint before expiry. Do not
assume an access-token-only rclone configuration can refresh itself. Handle Google
401 errors by renewing through core, with bounded retries. Module disablement or
grant refusal must stop existing rclone workers and discard runtime credentials.
The shared core contract is ready; this rclone adaptation remains module work.

## Revocation and limits

- Unlinking an identity deletes its grants through a database foreign-key cascade.
- Recreated Linux accounts cannot inherit grants; account epoch changes require
  reconnection. Current Linux availability is checked on every token request.
- Disabling a module prevents token delivery/refresh; re-enabling the same
  installation can resume valid grants. Removal and reinstallation change the
  installation identity and require consent again. Existing legacy installations
  use directory identity until the module manager writes an installation ID;
  the transition conservatively requires reconnection.
- Disabling Google prevents access. Saving provider settings changes the revision
  and requires reauthorization of earlier grants. Invalid refresh grants are
  marked `reconnect_required` and their stored token material is erased.
- Local revocation prevents further broker delivery/refresh. It is not a Google
  provider-wide revocation: already-issued access tokens can remain valid until
  expiry. The module must stop using them. Revoking a Google client grant directly
  can affect other permissions for that same application/account.

This protects normal API callers; it is not a sandbox against malicious root
modules or processes able to read core memory/state. Current modules can run as
root, and the planned single-service UID model also needs filesystem isolation.
Do not advertise isolation from privileged installed code.

## Validation boundary

Tests cover encrypted storage and ciphertext binding, subject/scope/offline
validation, owner/consumer isolation, replacement installations, unlink cascade,
cancelled consent, refresh rotation, cached reuse, transient failures, Google
revocation and account epoch changes. Google responses use signed local fixtures.
Existing real identity login was tested earlier; **real Drive consent and a real
Drive transfer are not yet verified**. The owner must select the account and
approve the new Google access when the Cloud Sync UI is ready.
