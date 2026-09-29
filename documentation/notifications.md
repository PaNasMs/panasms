# Notification delivery

Administrators configure SMTP, a Telegram bot and Web Push in **Settings → Notifications**. Each user configures destinations and routing in **My profile → Notifications**. Credentials are encrypted in the core database and never returned by the settings API.

## Default routing

| Severity | External channel |
| --- | --- |
| Information | None; panel only |
| Warning | Browser push |
| Error | Email |
| Critical | Telegram |

Each severity can select any combination of email, Telegram and browser push. The table shows initial defaults; existing single-channel choices are preserved when upgrading. An empty selection means panel-only delivery. Each selected channel has its own delivery status and retry schedule. Users may change this mapping. All events remain available in the panel. An unavailable channel produces a delivery error instead of silently forwarding private content elsewhere. External delivery is disabled until configured and enabled.

Messages use the recipient's current English, Russian or Ukrainian interface language, with English fallback. Administrators receive system events; other users receive their own task events. Account identity and event visibility are checked again before sending.

Administrators can send a test email directly from the SMTP settings to an explicit
recipient. Save and enable SMTP first. This test does not require personal delivery
to be enabled; it reports SMTP acceptance or a delivery error immediately. Acceptance
is not a guarantee of inbox placement; check spam as well.

## Telegram account linking

Users connect Telegram in **My profile → Notifications** (also available to the
current administrator in notification settings). Start linking, send `/link CODE`
to the configured bot in a private chat, then return to the NAS and confirm the
account name. A code expires after ten minutes and is replaced by the next code.
No recipient list or manually entered Telegram ID is needed. Tests always target
the current signed-in user's linked chat, independently of personal delivery enablement.

The shared Hermes bot uses `backend/integrations/hermes-telegram-link`, a native
Hermes plugin registered through `register_platform_handler`. Its `/link` handler
runs before the model and never starts another Telegram poller. Set `nas_url` in
its adjacent `config.json` and enable the plugin with `hermes plugins enable
panasms-telegram-link`. Keep the same bot configured on the NAS. Other bot owners
need an equivalent relay; an arbitrary existing bot cannot process `/link` without it.

The relay signs its raw JSON with HMAC-SHA256 using the configured bot token and
the `panasms-telegram-link-v1\n` domain separator. A timestamp limits replay;
only an unexpired challenge can record a candidate, and the NAS user must confirm
it before notifications can use the chat. This permits linking but does not grant
access to Hermes conversations/tools. Bot-token replacement invalidates prior
links. Account UID/principal changes cannot inherit a previous user's link.
The current LAN uses HTTP: the signature prevents modification but does not hide
relay metadata; deploy HTTPS when transport confidentiality is required.

Disconnect removes the link and cancels pending Telegram messages. The next send
rechecks the linked destination. Previously entered manual chat IDs are no longer
used; reconnect once through the verified flow after this upgrade.

## Reliability

The SQLite outbox survives service restarts. Stable alert states are deduplicated; a severity change or a resolved/reopened condition can generate a new event. Enabling notifications does not backfill old history. Failed sends have bounded exponential retries, a 24-hour expiry and a visible history with manual retry. Settings changes cancel queued messages. History is retained for 30 days.

Delivery is not exactly-once: if a provider accepts a message immediately before the core crashes, a retry can duplicate it. Provider acceptance also does not prove that a person read the message.

## Transports and limitations

- SMTP requires TLS or STARTTLS and certificate validation.
- Telegram uses `sendMessage` to a personal chat; the NAS does not consume bot updates; the existing bot owner relays linking commands.
- Web Push uses VAPID, encrypted subscriptions and a service worker. Registration requires a browser-trusted HTTPS origin and user permission. Plain HTTP on a LAN IP cannot register push. Supported endpoint families are Google FCM, Mozilla, Apple and Windows.
- The source is the core persistent alert/task stream. A module's private toast is not automatically an externally deliverable event.
- Transport settings are separate from per-user destinations. Changing a user's language affects future messages.

## Validation status

Queue persistence, deduplication, retries, account isolation, secret handling, routing and localization have automated tests. Core/API/store tests and the frontend production build pass. The ARM64 core was built and tested on the NAS and deployed on 2026-09-29.

Live SMTP, Telegram and push delivery still require configured endpoints. No reusable SMTP or Telegram notification connection was found on the NAS. The current HTTP NAS address cannot support browser push; HTTPS remains a separate setup step. Do not treat a successful build as proof of delivery to a real provider.
