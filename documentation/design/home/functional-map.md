# PaNasMs UI — functional map (source of truth: code at frontend 92c72b0 + modules, 2026-10-04)

Compiled by Claude for the visual redesign. Purpose: the redesign must carry every function below.
Labels are the real English strings. File references are relative to the workspace root.

## 1. Shell

**Taskbar** (`frontend/src/application.tsx`, `app/application-bar.tsx`), left to right:

| Part | What it does |
| --- | --- |
| Launcher ("Applications" today; owner wants "Sections") | Grid of every section with icon and name; ⋮ per entry opens the pin menu |
| Desktop link | Goes to `/` |
| Pinned sections | Icon links; reorder by drag or Alt+←/→; right-click menu with "Show in taskbar" and "Show on desktop" |
| Ongoing tasks | Up to 2 chips with icon, percent and progress bar, then "+N"; sources: uploads, file batches, core update, RAID sync/reshape, long jobs |
| Module indicators | Terminal: "Active terminals: N" popover (Return / Close all). Containers: job chip |
| Removable devices (admin, only when present) | Dropdown per device: Mount, Eject, file-system error repair |
| Tasks | Popover: uploads, module tasks, system tasks, job cards with Cancel / Check state; "Clear completed task history" |
| Notifications | Popover: severity, message, time; open related section, dismiss; "Clear history" |
| Profile | "My profile", "Sign out"; admins also "Shut down", "Restart" |

Pinning is per user (`preferences.taskbar`). Below 640px the pinned sections are simply hidden today;
the overflow menu required by the standard (NAV-01) is not implemented.

**Desktop** (`app/dashboard.tsx`, `app/desktop-layout.ts`): coordinate grid, 112×100px cells.
Three independent layouts per user: mobile (<640px, 2 columns), medium (<1100px, 6), wide (8).
Edit mode: add widget, move, remove, default layout, wallpaper upload/reset, save or discard.

Widget kinds: Time and date · Processor · Memory · CPU cooling · Uptime · HDD cooling · System drive ·
Disk activity · Temperature per disk (one per physical disk) · Network · shortcuts to every section.
There is NO array widget yet (owner wants one added).

## 2. Sections and their sub-navigation

| Section | Route | Sub-navigation today | Items |
| --- | --- | --- | --- |
| Desktop | `/` | none | — |
| Metrics history | `/history` | none (Period select) | Hour / Day / Week |
| Disks and storage | `/storage/…` | TOP TABS | Disks and arrays · Partitions and mounts |
| Users | `/users/…` | TOP TABS | Users · Groups; user detail has its own top tabs: Profile and groups · Security and access · SSH keys · Sessions · Security history |
| Shared folders | `/sharing` | TOP TABS | Folders · Connections |
| Network | `/network/…` | TOP TABS | Interfaces · Routes |
| System | `/system/…` | TOP TABS | Services · Logs · Updates |
| Settings | `/settings/…` | LEFT LIST | General · Users · Disk subsystem (nested top tabs: Settings · Advanced settings) · Notifications · External connections (nested top tabs: Google · GitHub · Dropbox) · System updates · Containers and applications (from the module) |
| My profile | `/profile/…` | LEFT LIST | Account · Appearance · Security · Connections · Notifications · Sessions & history |
| Modules | `/modules` | none (filter select); detail page | All / Installed / Not installed |
| Files | `/files` | own sidebar (places tree) | Places · Pinned folders · Trash · Devices |
| Terminal | `/terminal` | custom session tabs | Terminal N, + |
| Cloud Sync | `/cloud-sync` | LEFT LIST OF OBJECTS | one entry per sync task, then connections without tasks |
| Containers and applications | `/containers/…` | LEFT LIST | Containers · Images · Networks · Volumes · Tasks; container detail has link tabs Details · Logs · Settings |

So the same job — "switch between parts of one section" — is done three ways: top tabs (5 sections),
left list (3 sections), left list of objects (1), and two sections nest top tabs inside a left list.

## 3. Objects and actions (condensed)

- **Storage / disks**: disk card (type badge, state and SMART icons, temperature, details; SMART dialog with
  short/extended test, attributes, results; eject). Selecting unused disks shows a bar: Create array, Expand
  RAID, Add spare disk. Array: Replace selected disk, Change RAID level, Check array / Stop check, Delete array,
  Pause/Resume reshape; progress during sync.
- **Storage / partitions**: tree per device; selection bar with actions by type — free space (Create partition /
  file system / encrypted volume), file system (Mount, Unmount, Mount options, Size, Format, btrfs snapshots),
  LUKS (password, key, auto-unlock, header backup/restore, unlock, lock), partition (Size, Delete), Wipe device,
  network shares (Mount network share, Unmount). System partitions show a protection notice instead of actions;
  free space on the system drive is editable (see core-lifecycle.md, "System drive protection").
- **Users**: cards; Create user/group; detail with groups, home folder move, delete, numeric ID, reset password,
  SMB access, SSH keys, sessions, security history.
- **Shared folders**: share card (Edit in two steps: folder+protocols, access; Linux folder permissions; Stop
  sharing); unmanaged NFS exports; Restore managed configuration; SMB sessions (Disconnect).
- **Network**: interface card (details, edit connection, Wi-Fi switch and networks, disconnect, share
  connection wizard); sharing groups; timed confirm/rollback bar; read-only routes table.
- **System**: services table with actions and jump to logs; logs with four filters; OS updates table.
- **Settings**: HTTP port; CPU cooling profile; home folder location and move; disk cooling, disk sleep, SMART
  schedule, hardware cooling, polling interval, CRC baseline; SMTP/Telegram/push; OAuth clients per provider;
  system updates (check, download, install, rollback, channel, automation, history); Docker data location.
- **Modules**: repositories, install from archive, card actions (install/update, enable/disable, remove),
  review dialog, detail page with dependencies.
- **Profile**: avatar, name, theme, wallpaper, language, password, SSH keys, linked accounts and module
  permissions, delivery rules, push devices, delivery history, sessions.
- **Files**: places/devices/pins/trash sidebar, breadcrumb path, toolbar and context menus (create, upload,
  open, download, rename, copy/move, restore, delete, pin, permissions, share, hidden, list/icons, sort),
  drop menu with conflict choice, cloud places.
- **Terminal**: session tabs, reconnect, close all from the taskbar.
- **Cloud Sync**: tasks and accounts; pause/resume, sync now, remove, add-task wizard in three steps; history.
- **Containers**: containers (start/stop/restart/remove), compose projects (edit), images, networks, volumes,
  create dialogs, detail (metrics, ports, logs, settings), Docker engine banner.

## 4. Cross-cutting components in use

Dialog (compact / form / details, with busy overlay and discard guard) · operation dialog (parameters → plan →
confirm) · folder picker and folder field · multi-select · tables (8 places) · cards (disk, array, network,
share, user, group, module, key, job, notification, desktop tile) · status icon with tooltip · badge ·
status label · toast (max 3, 8s) · waiting overlay / surface · tooltip layer · notices used as empty states.

Six confirmation patterns exist: plan→Confirm; Yes/No; Cancel/Confirm; password-gated; timed rollback;
router "Discard changes?".

## 5. Findings that matter for the redesign

- Sub-navigation is the largest structural inconsistency (table in section 2). Decision by owner: ONE
  component everywhere; left or top does not matter as long as it is uniform.
- Icon-only actions dominate (array, disk, share, module, network cards). On a phone these need labels or a
  labelled menu (CMP-01 in the standard).
- Selection bars (storage) and the timed-confirm bar (network) are page-level floating elements that need a
  place in the phone layout.
- Two toast implementations (core and Containers), two folder trees outside the shared picker (Files, Cloud
  Sync), `ConfirmDialog` used in one file only, empty states are ad-hoc notices.
- Dead code: `app/pages.tsx` old Dashboard and its `.desktop-grid` rule.
- Docs drift: `feature-status.md` says Dropbox is hidden and GitHub sign-in is planned — both are present in
  the UI; Containers has no "Applications" view; the journal has no refresh control.
