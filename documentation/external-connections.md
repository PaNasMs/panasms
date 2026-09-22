# External connections

For a screenshot-based walkthrough, start with
[Set up Google sign-in for your NAS](google-sign-in-setup.md).

PaNasMs owns provider application settings, external identity bindings and the
browser authorization lifecycle. Modules must not maintain separate copies of
NAS-wide OAuth client credentials. The first provider is Google; this release
implements account linking and panel sign-in, not Google Drive synchronization.

## Administration and user workflow

An administrator creates a **Web application** OAuth client for this NAS in
Google Cloud Console. Register this exact authorized redirect URI:

```
https://panasms-oauth-gateway.panasms.workers.dev/callback
```

Enter Client ID and Client secret in **Settings → External connections** and
enable Google linking/sign-in. There is no shared application secret in the
package. An empty secret field preserves the saved secret only if Client ID is
unchanged. Changing settings invalidates outstanding authorization attempts.
Disabling Google prevents new linking and Google sign-in; existing panel sessions
keep their normal expiry and can be revoked through the session manager.

A signed-in user opens **My profile → Connections**, confirms their current
Linux password, and authorizes Google in a separate tab. If the browser blocks
that tab, the dialog includes an explicit link. The original panel polls for the
result. A Google account can be linked to only one Linux identity on this NAS;
multiple distinct Google accounts can be linked to the same Linux user.

The login page shows **Sign in with Google** only while the provider is enabled.
Unlinked accounts cannot create Linux users or inherit privileges by matching
email addresses. Local password login remains available, including when Google
or the internet is unavailable. Unlinking requires the Linux password and revokes
all panel sessions belonging to that user.

## Ownership and authentication

Connections use an opaque ID and `(provider, subject)` identity. Google email/name
are display metadata; the stable OIDC `sub` is the binding key. The binding also
records Linux username, UID and the account's persistent principal marker. A
recreated account must not inherit the previous account's connections. The agent
rechecks Linux/PAM account availability on Google sign-in, and ordinary session
checks continue to enforce account status, panel permissions, UID and epoch.

This flow requests only `openid email profile`. It validates the ID token's
signature, issuer, audience, expiry, nonce and verified email using the Go OIDC
library. Authorization uses PKCE S256. Google access/refresh tokens are not needed
for subsequent panel login and are not retained by this identity-only flow.
Google sign-in does not change Linux/SMB passwords or grant access to Drive/Gmail.

## Relay and browser binding

The fixed HTTPS relay receives `code` and opaque `state`, never the client secret
or resulting tokens. The NAS exchanges the code directly with Google. The relay
is an existing separate project; its code is not shipped in the core package.

Each attempt has an independent cryptographically random state, nonce, PKCE
verifier and browser ticket. A same-site HttpOnly cookie holds the browser ticket;
the core retains the attempt for at most ten minutes. Linking is also bound to
the initiating panel session and Linux identity. Origin/header checks cover all
mutating endpoints, including unauthenticated login start/poll/cancel. Starts and
password proofs are rate-limited; pending attempts are bounded and concurrent
polls serialized. Restart, expiry, cancellation and configuration changes abort
the attempt. A cancelled in-flight exchange cannot establish a session.

Cloudflare KV is eventually consistent and `get` followed by `delete` is not an
atomic consume operation. The core independently rejects repeated completion;
polling tolerates delayed visibility. The relay's claim of exactly-once delivery
must not be relied upon. A future gateway revision should use an atomic mechanism
for consumption. Transport failures are reported without exposing codes, tokens,
client secrets or provider response bodies.

## Storage and backup

Core SQLite migration `external-connections` creates `external_providers` and
`external_connections`. Client secrets are encrypted using AES-256-GCM, with the
provider identifier as authenticated associated data. The random local key is
stored alongside the database as `state.db.external.key`, mode `0600`, inside the
core's private state directory. The key must be included in protected system
backups together with the database. A missing or invalid key fails closed.
Encryption does not protect against an attacker who can read both the database
and the key or execute code as the core service user.

Public HTTP responses never return client secrets. Settings are administrator-only;
connection listing and unlinking are scoped to the current Linux identity. Settings,
link/unlink and successful/denied bound-account sign-ins use the security history.

## HTTP contract

The OpenAPI document in `backend/api/openapi.yaml` is authoritative. All POST/PUT/
DELETE calls require the normal same-origin and `X-PaNasMs-Request: 1` headers.

| Endpoint | Consumer | Purpose |
| --- | --- | --- |
| `GET /api/v1/external/providers` | Public login screen | Enabled provider flags |
| `GET/PUT /api/v1/external/settings/google` | NAS administrator | Client settings; secret is write-only |
| `GET /api/v1/external/connections` | Signed-in user | Owned identity connections |
| `DELETE /api/v1/external/connections` | Signed-in user + Linux password | Unlink and revoke panel sessions |
| `POST /api/v1/external/google/start` | Login screen or signed-in user | Start `login` or password-confirmed `link` |
| `POST /api/v1/external/google/poll` | Browser holding the flow cookie | `202 pending`, `200 linked/authenticated`, or explicit failure |
| `POST /api/v1/external/google/cancel` | Browser holding the flow cookie | Cancel, including an in-flight exchange |

## Cloud Sync handoff and extension boundary

Cloud Sync refactoring is a separate work item. Its existing per-user workers and
local authorization helper are unchanged by this core implementation. The prior
proposal to put NAS client settings and the entire OAuth flow inside Cloud Sync
is superseded by this shared core architecture.

A Cloud Sync grant is **not** the same thing as an identity connection. Before
using a linked account for Drive, extend the core with explicit consent for the
requested scopes and a grant bound to connection ID, consumer module ID and owner.
Keep token storage/refresh in the core and expose a narrowly authorized service
contract through the SDK. Do not send refresh tokens/client secrets to browser
code, grant every module access to all connected accounts, or let modules choose
arbitrary token endpoints/scopes. No general token-export endpoint exists yet.

An initial grant model should record `connectionId`, `consumer`, `scopes`, status,
encrypted token material and token expiry. Consumer enablement/removal and account
unlinking must stop refresh/use; already-issued access-token validity must be
accounted for. Personal and system-owned grants need explicit separate ownership
and permission policy, even if Cloud Sync uses one service account and one database.

Google External apps in Testing receive seven-day refresh tokens when requesting
Drive scopes. Identity-only scopes are exempt from that specific limit. Plan the
publishing/verification and scope policy before claiming unattended long-term
Drive synchronization works. Test consent and sync using real provider accounts.

## Validation

Regression tests exercise encrypted storage/tampering, missing keys, account
recreation, cross-user isolation, unlink session revocation, PKCE/scopes, signed
OIDC claims, replay, cancellation during exchange, credential changes, polling
failures and blocked/recreated Linux accounts. These use local provider fixtures;
passing them is not a claim of live Google consent acceptance for a user's client.

References: [Google web OAuth](https://developers.google.com/identity/protocols/oauth2/web-server),
[Google token lifetime](https://developers.google.com/identity/protocols/oauth2#expiration),
[Cloudflare KV consistency](https://developers.cloudflare.com/kv/concepts/how-kv-works/#consistency).
