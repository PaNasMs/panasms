# External connections

For a screenshot-based walkthrough, start with
[Set up Google sign-in for your NAS](google-sign-in-setup.md).

PaNasMs owns provider application settings, external identity bindings and the
browser authorization lifecycle. Modules must not maintain separate copies of
NAS-wide OAuth client credentials. Google and GitHub support account linking and
panel sign-in; Dropbox supports account linking. File/repository permissions are
separate capabilities, not implied by an identity connection.

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

The login page shows **Sign in with Google** and **Sign in with GitHub** only while the respective provider is enabled. Dropbox is available for account linking only.
Unlinked accounts cannot create Linux users or inherit privileges by matching
email addresses. Local password login remains available, including when Google
or the internet is unavailable. Unlinking requires the Linux password and revokes
all panel sessions belonging to that user.

## Provider capabilities and setup

| Provider | Account linking | Panel sign-in | Identity scope / stable identifier |
| --- | --- | --- | --- |
| Google | Multiple accounts per Linux user | Yes | `openid email profile` / verified OIDC `sub` |
| GitHub | Multiple accounts per Linux user | Yes | `read:user` / numeric account `id` |
| Dropbox | Multiple accounts per Linux user | No | `account_info.read` / `account_id` |

All providers use the existing callback relay:
`https://panasms-oauth-gateway.panasms.workers.dev/callback`.
A NAS does not need an inbound public address. The relay never receives application
secrets or access tokens. Its existing callback and automatic tab closing work
without a provider-specific deployment.

For GitHub:

1. Open [Developer settings → OAuth Apps](https://github.com/settings/developers)
   and register an OAuth App for this NAS.
2. Set **Authorization callback URL** to the exact relay URL above.
3. Generate a client secret. Enter **Client ID** and **Client secret** in
   **Settings → External connections → GitHub**, enable the provider, and save.
4. Sign in to PaNasMs with the Linux password, then link the account in
   **My profile → Connections**. After linking, GitHub can be used for panel login.

For Dropbox:

1. Open the [App Console](https://www.dropbox.com/developers/apps) and create a
   scoped app. Enable the `account_info.read` permission.
2. Add the exact relay URL above to the app's OAuth redirect URIs. Ensure that
   the intended Dropbox accounts are allowed to authorize the app.
3. Enter **App key** in the NAS **Client ID** field and **App secret** in
   **Client secret**, enable Dropbox, and save.
4. Link each desired account from **My profile → Connections**.

Linking always requires the current Linux password. GitHub names and email
addresses are display metadata, never login matching keys; a private or missing
GitHub email does not prevent linking. Dropbox linking requires a verified email.
Client secrets are encrypted separately per provider. Pending flows are bound to
the provider as well as the browser/session: polling or cancelling through another
provider's endpoint cannot complete or destroy the original flow. Changing a
provider's credentials invalidates only its own pending flows.

GitHub and Dropbox identity access tokens are used only to retrieve the account
identity and are not stored. Linking does not grant file/repository/SSH-key access.
Future module capabilities require separate explicit consent and token contracts.
There is no new database migration; existing provider-keyed tables support these
connections. New providers are disabled until an administrator configures them.

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
or resulting tokens. The NAS exchanges the code directly with the selected provider. The relay
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
| `GET/PUT /api/v1/external/settings/{provider}` | NAS administrator | Client settings; secret is write-only |
| `GET /api/v1/external/connections` | Signed-in user | Owned identity connections |
| `DELETE /api/v1/external/connections` | Signed-in user + Linux password | Unlink and revoke panel sessions |
| `POST /api/v1/external/{provider}/start` | Login screen or signed-in user | Start `login` or password-confirmed `link` |
| `POST /api/v1/external/{provider}/poll` | Browser holding the flow cookie | `202 pending`, `200 linked/authenticated`, or explicit failure |
| `POST /api/v1/external/{provider}/cancel` | Browser holding the flow cookie | Cancel, including an in-flight exchange |

## Module permissions

Consumer-bound Google Drive grants, encrypted token custody, refresh and a private
Unix token broker are implemented separately from identity connections. See
[External permissions for modules](external-grants.md) for browser/SDK contracts,
revocation behavior, limitations and the remaining rclone adaptation.

Cloud Sync uses per-user Go workers and the core grant broker. Linking an identity
does not silently create a Drive grant or expose tokens to modules. Dropbox file
permissions and GitHub repository permissions are not implemented by this change.

## Validation

Regression tests exercise encrypted storage/tampering, missing keys, account
recreation, cross-user isolation, unlink session revocation, PKCE/scopes, signed
OIDC claims, GitHub/Dropbox API identities, provider isolation, multiple account linking, replay, cancellation during exchange, credential changes, polling
failures and blocked/recreated Linux accounts. These use local provider fixtures;
passing them is not a claim of live Google consent acceptance for a user's client.

References: [Google web OAuth](https://developers.google.com/identity/protocols/oauth2/web-server),
[Google token lifetime](https://developers.google.com/identity/protocols/oauth2#expiration),
[Cloudflare KV consistency](https://developers.cloudflare.com/kv/concepts/how-kv-works/#consistency).
