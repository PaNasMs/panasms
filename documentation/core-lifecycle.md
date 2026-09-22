# Core contracts and recovery

The core HTTP service runs without root privileges. Authenticated requests reach a
separate privileged agent, which refreshes Linux permissions and validates the
operation against current system state before executing it. Installed modules
own their domain-specific APIs; the core owns job acceptance and tracking.

## API contract

[OpenAPI](https://github.com/PaNasMs/backend/blob/main/api/openapi.yaml) describes
built-in management snapshots, previews, job IDs, task states, recovery reports and
WebSocket messages. `ManagementViews` maps query names to their response schemas.
The frontend generates types from this contract. Native smartctl/Samba reports
retain extensible fields because supported data depends on the device and installed
system utilities. Action parameters remain validated by the owning domain handler.

A client previews an operation, confirms that preview, and submits a unique ID.
If a connection is lost, it queries that same ID before deciding what to show.
Resubmitting the same ID never replays a completed or hidden operation. Unknown
POST modes are rejected. A full queue returns 429; an unavailable task journal
returns 503. An uncertain response is not proof that an operation did not start.

The WebSocket carries versioned invalidations and metric snapshots, not commands.
After every reconnect, clients reread HTTP snapshots. Durable event replay is not
needed for this model: the authoritative job and configuration state is persisted.

## Persistence and migration

Core state and task history have separate SQLite databases. Both use WAL, FULL
synchronous writes and an immediate transaction for migrations. Each migration
records its component, sequence, name and SQL checksum. Historical migrations are
immutable; new changes append another version.

An upgrade either commits all pending migrations or leaves the previous schema
and data intact. Unknown newer versions, gaps, changed checksums and databases
belonging to another component are rejected. The previous core schema marker is
retained only for legacy compatibility. An application downgrade uses the updater's
matching package, configuration and database backup; it does not attempt reverse
SQL migrations against newer data.

## Task concurrency and interruption

At most four helper operations run concurrently. File/account work can coexist
with SMART commands. Mount/storage changes exclude operations using volumes;
unknown module actions and system/service/package changes acquire the exclusive
system claim. Conflicting queued requests keep their order so later readers cannot
starve a waiting writer. These locks coordinate panel jobs; external tools and
kernel maintenance must still be rechecked by domain preflight validation.

The agent persists `running` before launching a helper. A failed journal write
suspends new mutations until database access is restored and the agent restarts.
Already running helpers retain their safe completion/cancellation rules. Output
is bounded without killing a helper during a potentially irreversible commit.

After restart, queued jobs become cancelled-before-start and running jobs become
interrupted. Neither credentials nor executable requests are replayed. Unreviewed
failures remain visible when history is cleared. Recovery inspection is read-only;
repair actions require a new preview and explicit confirmation.

Domain journals handle home moves, modules, shared-folder configuration, network
rollback and independent core updates. Storage inspection reports the actual
RAID/partition/filesystem state. Formatting, deletion and partially completed RAID
changes are not generically reversible; automatically rerunning them is unsafe.

## Verification boundary

Automated checks cover fresh/legacy databases, successful and failed migrations,
future/changed-schema refusal, real subprocess death inside a migration and job,
journal failure before and after helper execution, duplicate submissions,
user ownership, cancellation, exclusive ordering and independent concurrency.
Contract checks exercise production query functions and validate schema coverage.
Read-only snapshots from the test NAS were also checked against the contracts.

Physical power cuts, defective media/controllers and the complete destructive
storage compatibility matrix remain hardware/production acceptance tests. SQLite
sync guarantees depend on the OS and storage device honoring flush requests.
No physical power cut or destructive RAID test is part of a routine software update.
