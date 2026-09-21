# PaNasMs UI/UX guidelines

Version 1.1 · 2026-09-21 · Pavlo's NAS Management System

**Status:** accepted design baseline. This guide defines requirements; it does
not claim that every existing screen already conforms or has passed accessibility
acceptance. Public documentation is English; the interface supports English,
Russian and Ukrainian.

This is the canonical public guideline for core and module UI contributions.
Internal audits, deployment records and feature-delivery plans are maintained
separately and are not part of this publication.

## How to use this guide

**MUST** is a requirement for a screen being brought into conformance with this
guide. **SHOULD** is the default; document a concrete reason for an exception.
**MAY** is optional. These words describe our project rules, not an assertion that
every rule is a legal or external standard.

WCAG requirements are identified separately. Numeric sizes, breakpoints, colors,
timings and action placement below are **PaNasMs design decisions**, not numbers
prescribed by usability research. Validate them with realistic content and tasks.
Existing user decisions take precedence over examples in external design systems.
A guideline change does not itself authorize changes to a running NAS.

### Contents

1. [Product principles](#1-product-principles)
2. [Navigation and ownership](#2-navigation-and-ownership)
3. [Visual foundations](#3-visual-foundations)
4. [Components and interactions](#4-components-and-interactions)
5. [Forms and settings](#5-forms-and-settings)
6. [Waiting, tasks, feedback and recovery](#6-waiting-tasks-feedback-and-recovery)
7. [NAS-specific patterns](#7-nas-specific-patterns)
8. [Accessibility and localization](#8-accessibility-and-localization)
9. [Shared implementation contract](#9-shared-implementation-contract)
10. [Research basis and deliberate adaptations](#10-research-basis-and-deliberate-adaptations)

## 1. Product principles

**P-01 — Start with the user's task. MUST.** Design for an owner administering a
home NAS and an ordinary user accessing permitted files. Primary tasks include
checking health, finding data, attaching storage, managing access and recovering
from an interrupted operation. Do not require knowledge of Linux commands to
complete a supported task. Show technical identifiers when they disambiguate a
target or explain a problem.

**P-02 — Simple first, detail on demand. SHOULD.** The first view answers: what is
this, what state is it in, and what can I do next? Advanced parameters remain
available near their subject. Never hide an important consequence in Advanced.
This applies KDE's approach to progressive complexity to our web application,
without adopting its Qt-specific component or navigation rules.
[KDE: Simple by default](https://develop.kde.org/hig/simple_by_default/)

**P-03 — Familiar and consistent. MUST.** One object, action or state has the same
name, icon, behavior and identity in every module. A USB drive in Files and the
removable-device menu must match Storage. Reuse our existing MDI icon family.
Inspiration from DSM and Dolphin concerns interaction patterns; their artwork and
branding are not our design system.

**P-04 — Compact, readable, stable. MUST.** Remove duplicated information before
shrinking text. Keep related controls together. Loading, selection and background
updates must not unexpectedly move the object under the pointer. Compactness does
not justify illegible labels or tiny click targets.

**P-05 — Show what is known. MUST.** Distinguish configured intent, observed state,
pending changes and stale data. Unknown health is not healthy; missing temperature
is not zero; a request timeout is not proof that a disk operation stopped.

**P-06 — Preserve control. MUST.** Keep the target and consequences clear, retain
form input after errors, and expose supported recovery. Never offer Undo, Cancel,
Pause or Retry unless the backend can perform the corresponding operation safely.

## 2. Navigation and ownership

**NAV-01 — A stable shell. MUST.** Keep the agreed top bar: application menu,
Desktop shortcut, user-pinned module shortcuts, separator, compact ongoing tasks,
then task/notification/removable-device controls and the user menu. Removable
devices appear when relevant. Do not restore the removed logo or permanent
“online” label. The application menu provides visible module names; taskbar icons
are shortcuts to these named destinations. On narrow screens, move excess pinned
shortcuts into a named overflow menu before squeezing controls.

**NAV-02 — Pages for places; popovers for quick activity. MUST.** Modules and
Settings use the same page shell. Tasks, notifications and removable devices stay
top-bar popovers, with details opened only when needed. A long module details view
is a page. A brief SMART or interface inspection is a dialog. Do not introduce a
separate application window system or a giant universal management dialog.

**NAV-03 — URLs describe the working location. MUST.** Major sections, subsections
and meaningful detail views are addressable. Refresh and browser Back/Forward
restore the view. Use path segments for hierarchy and query parameters for view
state such as a selected account, filter or folder; reuse the existing route
helpers. Do not put passwords, tokens or destructive command intent in URLs.
Opening a URL never repeats a write operation. Preserve scroll and useful list
state when returning from details. Handle missing objects and unavailable modules
with a clear message and a working route back.

**NAV-04 — One home for each responsibility. MUST.**

| Area | Owns |
| --- | --- |
| Users and groups | Linux identity, membership, panel/SSH/SMB access, sessions |
| Storage: Disks and arrays | Physical devices, RAID membership and maintenance |
| Storage: Partitions and mounts | Partitions, filesystems, mount points and remote mounts |
| Shared folders | Publishing local folders over SMB/NFS and publication permissions |
| Files module | Browsing and file operations; permitted ownership/access editing |
| Network | Interfaces, Wi-Fi, routes and connection sharing |
| Settings | NAS-wide policy, with general/advanced subsections contributed by modules |
| Personal profile/preferences | Language, appearance, wallpaper and personal layout |
| Module manager | Catalog, installed versions, dependencies, installation and removal |

Link to the owning area instead of introducing a second editor with different
behavior. A file permission editor is not a separate user directory; Samba access
does not create a second visible set of people.

**NAV-05 — Reveal hierarchy once. MUST.** Breadcrumbs or a clearly named Back
control explain where a detail view belongs. Do not repeat the same hierarchy in
a sidebar, tiles and a second set of bars. Use trees for parent/child relationships,
cards for a small set of identifiable objects, and tables/lists for comparing many
records. Tables remain appropriate for users, logs and schedules; the accepted
Storage hierarchy is not to be replaced with a generic table.

### Page anatomy

~~~text
Persistent application bar
Page title                         Page-level icon actions
Optional short description
Section navigation, if needed
Filters / stable selection-action area, if needed
Main content: objects, hierarchy or form
~~~

The page header identifies the task. Decorative slogans and repeated descriptions
SHOULD be omitted. One primary page heading is enough.

## 3. Visual foundations

### VIS-01 — Shared tokens. MUST

Core and modules use semantic tokens, not independently selected colors or sizes.
The following values define the shared design baseline. The frontend semantic
tokens implement it; validate individual components against this specification. Use rem for typography and scalable spacing;
pixel equivalents assume the browser's default 16px root size.

| Token family | Baseline |
| --- | --- |
| Spacing | 4, 8, 12, 16, 24, 32, 48px; no arbitrary large gaps between form rows |
| Page padding | 24–32px on wide screens; 16px below 640px |
| Card padding / gap | 16px / 16px; compact member card padding 12px |
| Form label → control → help | 8px / 4px; 16px between fields; 24px between groups |
| Control height | Minimum 40px; minimum 44px for coarse-pointer/touch use |
| Icon hit area | 40×40px normally; 32×32px only in dense mouse-oriented rows; 44×44px on touch |
| Icon drawing | 20px in actions, 24px in navigation; hit area is larger than the drawing |
| Border radius | 8px controls, 12px cards, 16px dialogs; pills only for suitable badges |
| Borders / focus | 1px structural borders; separate 2px focus outline with 2px offset |
| Motion | 120–180ms for local transitions; respect reduced-motion preferences |
| Layer order | Page → sticky shell → popovers → modal backdrop/dialog → dialog popovers → toast |

A tooltip belongs above its own trigger's layer. A toast must not obstruct modal
actions. This is a semantic layer contract, not permission for modules to choose
arbitrarily large z-index values.

### VIS-02 — Typography. MUST

Keep Inter with system fallbacks. Use weight 400 for content, 500 for labels and
600 for headings. Do not use tiny uppercase text to carry necessary information.

| Role | Size / line height | Use |
| --- | --- | --- |
| Page title | 28 / 36px | One main heading; 24 / 32px on narrow screens |
| Section/dialog title | 20 / 28px | Clear heading, not a second page banner |
| Card title | 16 / 24px | Ordinary device/module card |
| Compact member title | 14 / 20px | RAID member, still readable |
| Body and input value | 16 / 24px | Descriptions, form input, decision text |
| Label and dense row | 14 / 20px | All form labels, controls, navigation labels |
| Secondary metadata | 12 / 16px | Timestamps and nonessential technical details only |

Input values stay at least 16px on mobile. Use tabular numerals for changing
metrics and progress. Preserve file extensions and distinguishing serial suffixes
when truncating. A compact RAID title may remain one line with an ellipsis; expose
the complete name in accessible details instead of shrinking it to 10px.
These sizes are our legibility choices; WCAG does not prescribe a universal
minimum font size.

### VIS-03 — Color roles and theme palette. MUST

| Role | Light | Dark |
| --- | --- | --- |
| Canvas | #F3F5F8 | #0C121D |
| Surface | #FFFFFF | #151E2C |
| Raised/subtle surface | #F5F7FA | #1D2939 |
| Primary text | #18283C | #E5EDF8 |
| Secondary text | #526176 | #A3B2C7 |
| Decorative divider | #D3DCE7 | #344258 |
| Essential control boundary | #788697 | #6F8198 |
| Primary action | #1D6A50 | #86DDB9 |
| Text on primary action | #FFFFFF | #0C121D |
| Focus / selection outline | #1D4ED8 | #93C5FD |
| Selection fill | #E8F0FF | #1A304D |
| Success | #18754B | #79D8A0 |
| Information / progress | #1D4ED8 | #93C5FD |
| Warning | #8A4B00 | #F2BD64 |
| Error / destructive action | #B42336 | #FDA4AF |

Use status colors on symbols and short status content, not on entire network
cards. A selected card uses the selection treatment plus a checkmark/border;
selection is distinct from health. Structural RAID grouping does not mean success.

Palette check on 2026-09-21: against both specified opaque surfaces, the lowest
text/status contrast is 5.31:1 in light and 6.83:1 in dark; control-boundary minima
are 3.46:1 and 3.69:1. Filled primary-button text measures 6.50:1 and 11.66:1.
These calculations do not validate every rendered combination, alpha blend,
selected state or user wallpaper. Decorative dividers are not control boundaries.

Normal text requires 4.5:1; qualifying large text may use 3:1. Essential non-text
control/state graphics require 3:1 against adjacent colors, with the standard's
exceptions. Check actual rendered pairs in both themes.
[W3C text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html),
[W3C non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)

### VIS-04 — Wallpaper and surfaces. MUST

Keep the user's wallpaper across the desktop and module pages, with the agreed
dimming treatment on both. Content surfaces and the shell must preserve readable
contrast independently of the image. Put headings on a controlled backing when
the scrim alone cannot guarantee contrast. Avoid relying on blur to make text
readable. Provide an opaque fallback and reduce decorative effects on constrained
hardware. Changing wallpaper is a personal preference, not a global NAS setting.

### VIS-05 — Responsive geometry. MUST

Use content-driven wrapping; the following are initial layout bands, not device
detection: under 640px single-column, 640–1023px intermediate, 1024px and above
wide. Recheck every band with translated text.

- Ordinary cards target a 240–360px width on wide screens. A lone card does not
  stretch across the page. At narrow widths it may fill the available column.
- An array is one outer layout item. Wrap the next standalone disk below the group
  before compressing array members. If the group itself cannot fit, reflow its
  members inside the group with a clear boundary; never scatter them outside it.
- Use comparable card heights within a row when content fits. Do not impose one
  fixed height on all cards or shrink text to preserve equal height at zoom.
- Main forms target a 640px reading width; related paired inputs may use a wider
  section. Keep controls near their labels instead of stretching every row.
- A page has one main vertical scrolling area. Trees and long data lists MAY have
  their own scroll area when useful. Do not create tiny scrolling panels inside
  cards while the surrounding page contains unused space.
- Dialogs fit the viewport with 16px outer clearance; scroll their body, keeping
  their title and decisions reachable. Avoid nested vertical scroll traps.

Support reflow at 320 CSS px and text zoom at 200%. Test 400% page zoom from a
1280px-wide viewport. Essential two-dimensional views, such as a terminal or data
table, may have contained horizontal scrolling; this is not an exemption for the
whole page. A desktop widget grid also needs a usable narrow-screen arrangement.
[W3C reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)

### VIS-06 — Tabs and elevation. MUST

Horizontal tabs and their content form one panel. The tab strip has a subtle
background, no outer padding and no gaps between tabs. Rectangular tabs occupy
its full height (minimum 48px), with thin vertical separators. The active tab
uses the content background and a 3px accent line at its top, joining the content
without a gap. Only the outer panel corners are rounded. Narrow strips scroll
horizontally without a scrollbar breaking that visual join; keyboard focus and
selected-tab reachability must be preserved.

Cards use the shared `--shadow-card` token and a subtle `--card-border`.
Interactive cards may use `--shadow-card-hover` on hover, without scaling or
moving. Menus and dialogs use the stronger `--shadow-raised`. The outer tabbed
panel and structural RAID grouping stay flat: avoid nested stacks of shadows.
In dark mode retain visible surface differences and outlines; shadows do not
replace selection, focus, control boundaries or status indicators.

## 4. Components and interactions

**CMP-01 — Icons are a compact language, not a guessing game. MUST.** Use one icon
for one meaning. Healthy state and the SMART action must differ. Disks, USB flash,
SD cards, arrays and remote folders have different object icons. Use a maintained
icon map shared by modules.

Icon actions require an accessible name and a tooltip available on hover and
keyboard focus. Prefer verb + object, such as “Eject USB backup”, to “Action”.
Do not use a native title attribute as the only explanatory mechanism. On touch,
unfamiliar actions must also be available in a labeled action menu. Primary
decisions in dialogs use visible text. The application catalog and desktop
shortcuts retain visible names.

This deliberately preserves the owner's compact toolbars while addressing icon
ambiguity. It is an adaptation, not a claim that research favors icon-only UI;
NN/g recommends persistent labels.
[NN/g: Icon usability](https://www.nngroup.com/articles/icon-usability/)

**CMP-02 — Tooltips add context, not controls. MUST.** Custom tooltips remain
available while hovered/focused, can be dismissed with Escape, and contain no
buttons or essential instructions that cannot be found elsewhere. For touch,
state details open through an explicit Details action. Do not make every status
symbol an extra keyboard tab stop; make its equivalent description available in
the object's accessible summary and details.
[W3C hover/focus content](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html)

**CMP-03 — Place actions by their scope. MUST.**

| Scope | Placement | PaNasMs example |
| --- | --- | --- |
| Whole view | Header toolbar | Refresh devices, install module archive |
| One object, frequent | Object header or row | SMART, eject, share connection |
| Selected object(s) | Stable contextual toolbar above collection | Create RAID, filesystem actions, move files |
| Rare secondary action | Named overflow menu | Less common maintenance |
| Multi-step dependency | Focused wizard starting at the object | Configure connection sharing |

Contextual actions appear only for meaningful selections; provide a short initial
hint explaining selection. Reserve their toolbar space or replace an existing
hint row so the collection does not jump. Show selection count and a clear-selection
control. A chosen object is passed into the action; do not ask for it again.
Do not add bulk selection where all actions are inherently per-interface.

**CMP-04 — Interaction states. MUST.** All interactive components define default,
hover, focus, pressed, selected where applicable, disabled and busy states. Focus
and selection remain visually distinct. Hide actions outside the user's role;
for a relevant but temporarily blocked action, show the reason in accessible text
or details. A disabled button's tooltip alone is insufficient. Unsupported
hardware features belong in capability details, not as a wall of dead controls.

**CMP-05 — Card anatomy. SHOULD.**

~~~text
Object icon + interface/type             Object actions
Object name / distinguishing identity
Primary value or relationship
State symbols + concise important metrics
Secondary facts only when useful here
~~~

Keep action order stable between peer cards. A whole-card selection target must
not contain nested interactive controls as part of one button. Activating SMART,
eject or a menu must not accidentally select, navigate or start dragging the card.

**CMP-06 — Popovers and menus. MUST.** Close on Escape and outside interaction,
return focus sensibly, keep the trigger's expanded state accurate and fit the
viewport. A command menu uses menu keyboard behavior. Tasks/notifications with
progress, links and multiple row controls are structured popovers, not ARIA menus
with arbitrary form elements forced inside them. Use normal Tab navigation there.
Only one top-bar popover is open at a time.
[W3C menu button pattern](https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/)

**CMP-07 — Dialogs. MUST.** A dialog has one named purpose and an object-specific
title, such as “Network details · wlan0”. Use initial width targets of 440px for
confirmation, 640px for a form, and at most 800px for substantial details; allow
smaller content-driven widths. Focus enters the dialog, remains inside, and
returns to its trigger or a logical successor. Provide a visible close/cancel
control. Escape dismisses ordinary dialogs. Never stack editors unnecessarily.
[W3C modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)

**CMP-08 — Confirmations. MUST.** Confirm destructive or disruptive intent once,
with the exact object, practical consequence and two clear decisions. Use a short
dialog; emphasize the object name. No typed paths, typed names or “type DELETE”
challenges. Prefer “Delete array” / “Cancel” over a generic “OK”; preserve a
deliberately agreed Yes/No prompt where its question already names the action.
Never place initial focus on permanent deletion. Ordinary navigation, opening
details and mounting a healthy device to the default location need no confirmation.

For deleting files, preserve the agreed compact choices: **Move to Trash**,
**Delete**, **Cancel**. If Trash is unavailable, explain why and offer permanent
deletion explicitly; do not silently substitute it. For bulk deletion, give a
count and an inspectable list. An optional Details disclosure may explain checks,
but must not hide the fact that data will be lost.

This adapts NN/g's emphasis on specific consequences and limited confirmation;
its typed-confirmation suggestion is intentionally not adopted, following the
owner's decision.
[NN/g: Confirmation dialogs](https://www.nngroup.com/articles/confirmation-dialog/)

**CMP-09 — Dragging and selection. MUST.** Show a drag preview and its actual
target, validate before accepting the drop, and preserve the source on rejection.
Desktop placement shows every occupied destination cell, with a non-color invalid
cue as well as red. Escape cancels. Provide click/tap alternatives: Move to folder,
Move before/after for shortcuts, and choose item then destination for the desktop.
Keyboard operation is required too; it does not replace the non-drag pointer
alternative required by WCAG 2.2.
[W3C: Dragging movements](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html)

**CMP-10 — Compact selection and complete tiles. MUST.** Group membership uses
a searchable multi-select with selected values and their count, not an always
expanded checkbox wall. Module cards separate name/version, explicit installed
and enabled states, and compact actions. Desktop shortcuts fill the entire grid
cell with one background covering both icon and label; widget footprints and
user placement remain unchanged.

## 5. Forms and settings

**FORM-01 — Clear fields. MUST.** Put persistent labels above inputs and keep all
labels at the same type scale. A placeholder is an example, never a label or the
only representation of the current value. Group related fields and their hints.
Distinguish required and optional input. Do not duplicate the page heading inside
every form or show boilerplate explaining implementation details.

**FORM-02 — Pick existing objects. MUST.** Choose users, groups, disks and folders
from appropriate selectors, with search when the list is long. Show display name
plus distinguishing identity. Allow path entry when useful to experts, but supply
a folder picker. Current settings populate their fields. A new folder dialog
asks for its name in the current directory, not a repeated full path.

**FORM-03 — Save semantics are explicit. MUST.** A switch means an immediate,
reversible state change; a checkbox in a Save/Apply form is a pending selection.
Do not mix both meanings without clearly separated sections. Put a switch beside
its label and state, not at the opposite edge of a large card. While applying,
prevent repeated submissions and distinguish the request from confirmed state.
Failures restore the observed value and explain the result.

Forms with several related changes have one Apply/Save action and an explicit
unsaved state. Preserve edits during background refresh; if server values change,
offer review/reload rather than silently overwriting input. Warn only when leaving
would actually discard edits. Use a neutral Cancel/Back action consistently.

**FORM-04 — Validate without blaming. MUST.** Explain constraints before submission
when they affect the choice. Validate on submit or after the user has left an
edited field; do not show errors before interaction. Keep entered values and
associate each error with its field. For long/multi-field forms add a linked error
summary and focus it; for a single-field dialog focus the invalid field and its
associated message. Backend authorization and validation remain authoritative.
Service failure or access denial is not an invalid input value.
[GOV.UK: Error messages](https://design-system.service.gov.uk/components/error-message/),
[GOV.UK: Error summary](https://design-system.service.gov.uk/components/error-summary/)

**FORM-05 — Policy lives with its subject. MUST.** Normal settings contain the
choices needed for ordinary use; Advanced holds timers, tuning and uncommon
options. Disk cooling and the common HDD idle timeout belong to disk settings.
Users' language/wallpaper stay personal. Do not invent password rules beyond the
host Linux policy. State when a setting requires a restart, is deferred during
RAID work, or affects more than the selected object. Apply capability-based
choices, such as allowed Wi-Fi channels, before the user reaches an error.

**FORM-06 — Filesystem destinations. MUST.** Use the shared visual folder picker
with a policy appropriate to the operation. Show existing roots and directories;
when creating a destination, ask only for the new folder name under the selected
parent. Explain disabled destinations. Home relocation rejects removable/USB,
remote, read-only, unavailable and nonpersistent volumes. Enforce these policies
again on the server when planning and executing; the picker is not a security
boundary. Selecting a location never creates or moves data by itself.

## 6. Waiting, tasks, feedback and recovery

### OPS-01 — Design every data state. MUST

| State | Required presentation and behavior |
| --- | --- |
| Initial loading | Stable placeholder geometry; a descriptive loading state |
| Loaded | Current data and available actions |
| Refreshing | Keep existing content and selection; do not replace the page with a spinner |
| Empty | Explain that there are no objects and provide the relevant next action |
| No filter results | Retain filters; offer clear/reset, not initial setup |
| Unsupported capability | Explain the specific limitation; do not imply hardware failure |
| No permission | Explain access and provide a valid route back, without leaking restricted data |
| Unavailable / disconnected | Identify what is unavailable and whether reconnection is in progress |
| Stale / unknown | Keep last-known data with its age and uncertainty; do not label it current |
| Read error | Explain the affected region and provide a safe retry |

Do not make an empty device list appear while a request is loading or failing.

### OPS-02 — Acknowledge and scope waiting. MUST

Give immediate pressed/busy feedback and prevent duplicate submission. As a
project timing target, show a waiting indicator after roughly 300ms if the request
is still pending. The threshold avoids flashes; it does not delay submission.

For an operation requiring the current dialog to wait, cover that dialog with the
agreed translucent overlay, spinner and specific message. Keep the affected
controls inert and communicate busy state to assistive technology. For a page
action, cover only its affected region. A local save must not block the entire NAS
shell. Elapsed time may be shown; it is not a progress percentage.

If the server accepts a background job, move to task presentation and allow the
dialog to close without cancelling the job. Do not trap the user behind a modal
for a RAID rebuild, upload or package installation. If a short foreground request
loses its response, leave indefinite waiting through an explicit “Checking result”
state with a safe way back to task/object status; do not infer failure or resubmit.
Suppress Escape only during a bounded submission transition, never indefinitely.

Use an actual progress bar only when measurable progress is available; otherwise
show a named phase and an indeterminate indicator. This adapts Carbon's distinction
between loading indicators, progress and the scope of the operation.
[Carbon: Loading patterns](https://carbondesignsystem.com/patterns/loading-pattern/)

### OPS-03 — Job state is a contract. MUST

Present the backend's applicable states distinctly: queued, running, pause
requested, paused, cancellation requested, cancelled, succeeded, failed and
interrupted/review required. This list defines UI meanings; it does not assert that
every job supports every transition or prescribe API enum names.

Show the object, action, phase, measured progress if available and supported
controls. Cancellation requested is not cancelled. Paused is not failed.
Retry creates or resumes work only according to the operation's recovery rules.
Separate pausing RAID maintenance from cancelling a file copy. Explain partial
results and remaining cleanup when cancellation cannot undo completed work.

Long tasks appear in the task menu and compact top-bar indicators: icon + percentage
when known, with a full accessible name/tooltip. Provide a phase in details when
percentage is unknown. RAID pause/resume sits beside its progress bar. There is
one authoritative job identity across the card, task menu and notification.
Reopening the page must reattach to existing work rather than starting it again.

### OPS-04 — Choose the right feedback channel. MUST

| Event | Presentation |
| --- | --- |
| Ordinary successful save | Brief toast and updated object; no persistent success panel |
| Field validation error | Inline field message, plus summary when appropriate |
| Recoverable action failure | Persistent explanation in the action context or task details |
| New device / completed long job | Toast plus a discoverable event/task entry |
| Ongoing hardware problem | Status on the object plus an active notification |
| Decision needed before proceeding | Focused dialog with explicit choices |

Use polite announcements for routine feedback; reserve assertive alerts for urgent
errors. Do not announce each metric tick. Our toast default is 8 seconds for short,
nonessential success text, paused while hovered or focused, with manual dismissal.
Do not put the only recovery action in an expiring toast. Retain important events
in history and actionable errors until they are resolved or explicitly dismissed.
Group repeated events; at most three visible toasts, with remaining events in the
notification menu. These limits are project choices.

This uses Carbon's distinction between transient feedback and contextual messages;
it does not require Carbon components or its visual styling.
[Carbon: Notifications](https://carbondesignsystem.com/components/notification/usage/)

### OPS-05 — Errors explain the next step. MUST

Give: **what could not happen → which object → why → what the user can do**.
Prefer “Cannot unmount Media: Cloud Sync is using this folder. Pause its task and
try again.” to “Operation failed” or a PID alone. If the cause cannot be identified,
say so; show verified process/service information in Details instead of guessing.
Provide copyable technical details/job ID for investigation, without exposing
passwords or tokens. Unexpected route/module errors have a recovery screen, not a
framework stack trace that replaces the entire shell.

### OPS-06 — Reconcile before claiming success. MUST

A change becomes successful only after the relevant backend result is known and
the affected view is refreshed. A WebSocket event invalidates the appropriate
data; reconnecting refreshes authoritative state. Preserve focus, selection and
editing during updates. Do not require a manual browser reload after removing a
schedule entry, mounting a device or finishing a repair.

Dismissed, acknowledged and resolved are separate concepts. Clearing history
removes eligible historical entries; it does not repair hardware or erase an
active problem. Accepted historical SMART counters must not reappear as a new
fault unless the monitored condition changes. A transient lost event stream must
not turn every healthy device into an error or discard a running job.

### OPS-07 — Timed rollback and interrupted work. MUST

Connection changes that need confirmation use a dedicated dialog with the
server's remaining rollback time, “Keep changes” and “Revert”. Explain the affected
connection before Apply. A browser refresh must not restart the timer. If the
backend supports an extension, expose it; otherwise document why the actual
connection-recovery deadline cannot be extended. The relevant WCAG timing rules
must be assessed for this flow rather than assuming that any countdown is exempt.
[W3C: Timing adjustable](https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html)

After interruption, show what completed, what is preserved, what is uncertain and
which recovery actions the backend supports. “Requires attention” must open useful
details. Do not offer a generic retry for an unknown destructive outcome or mark
a pending recovery as resolved when history is cleared.

## 7. NAS-specific patterns

**NAS-01 — Storage identity and hierarchy. MUST.** Keep physical drives/RAID and
partitions/mounts in their agreed separate tabs. Group array members inside the
array; put filesystem actions on the filesystem view. Show only real layers:
device or array → partition if present → filesystem → mount location. A filesystem
on a whole device does not need an invented partition. A remote mount shows its
server/share identity, not a fake physical disk.

Use friendly names plus stable distinguishing details; device paths may change.
Show raw drive capacity, usable array capacity and filesystem capacity at their
own layers. RAID expansion is not evidence that the filesystem grew. Existing
filesystem metadata can exist during synchronization; label observed state rather
than inferring readiness from RAID progress alone. Synology's drive/pool/volume
separation is useful precedent, not a reason to introduce unsupported pool types.
[Synology: Storage management](https://www.synology.com/en-global/dsm/7.4/software_spec/storage_management)

**NAS-02 — Health, power, access and activity are different. MUST.** Use independent
state dimensions and readable details rather than one ambiguous green dot.

| Dimension | Example values | Presentation |
| --- | --- | --- |
| Health | Healthy, warning, failed, not reported | Check, warning triangle, error, neutral no-data symbol |
| Power/presence | Active, sleeping, disconnected | Activity, sleep, disconnected symbol |
| Use/access | System device, array member, read-only, mounted | Role/access marker or hierarchy |
| Background work | Syncing, checking, paused | Progress/phase and supported controls |

Use shape and accessible text as well as color. A USB flash drive without SMART is
not faulty. Offline/disabled is not automatically an error; a missing required RAID
member is. Keep fault explanations and their affected scope visible in details.

**NAS-03 — Hardware-appropriate information. MUST.** Disk, USB and SD cards show
fields actually supported by that medium. Identify “not supported”, “not measured”
and “not currently available” distinctly in details; omit irrelevant rows in the
compact card. Show the time of cached temperature/SMART data. Routine UI refresh,
hover or opening a dashboard must not wake sleeping HDDs merely to refresh a
value. An explicit measurement that may wake a drive explains that effect.

Widget readings have units and a known/unknown state. CPU/HDD cooling widgets
display the agreed fan percentage, but distinguish commanded PWM output from
measured speed when telemetry cannot verify it. The HDD widget uses the hottest
available disk temperature and exposes stale/missing readings appropriately.

**NAS-04 — Removable-device flow. MUST.** Match device names/icons between Storage,
Files and the top-bar menu. With one usable partition, put mount/eject actions at
device level; with several, expose their individual filesystems. Mount healthy
filesystems at the default location without a configuration dialog. Eject first
unmounts affected mounted filesystems and reports named blockers before detaching.

Preserve the agreed compact eject confirmation. When discovery finds errors,
offer Repair or Skip; on a mount attempt with known errors, offer Repair,
Read-only or Cancel. Show repair progress and refresh the result. Do not repeat a
resolved repair warning after refresh. The UI must not claim safe removal until
the relevant operation is confirmed.

**NAS-05 — Network relationships. MUST.** Ordinary interface cards retain useful
inline facts. A sharing source card instead contains a vertical list of recipients;
source/recipient technical details open separately. Preserve recipient action
order: Wi-Fi settings when applicable, Remove from sharing, Details. Source
actions start on that source card, not in a global selection system.

The wizard asks for one meaningful decision per step, preselects known context and
offers only capabilities the hardware/backend supports. Show Wi-Fi enable state
next to its label; it belongs in Wi-Fi settings and affects that adapter only.
Distinguish disabled, unplugged, connecting, connected and connection failure.
Unplugging preserves a configured recipient with an absent state; explicit removal
explains what configuration is deleted. Returning hardware must update the same
object, not create an indistinguishable duplicate.

**NAS-06 — Files and the desktop. MUST.** The Files sidebar combines named entry
points and expandable device/folder trees. Separate expanding a node from opening
its contents. Keep Up and breadcrumbs available, one Trash entry, and consistent
remote-folder/RAID identities. Context menus mirror toolbar actions; they are not
the only way to reach a feature. Support keyboard invocation of the context menu.

File dragging offers a clear move/copy result and handles conflicts without silent
overwrite. Upload from the computer has a distinct drop target. Lazy thumbnails
load only for visible/near-visible tiles; list view uses type icons. Failed
thumbnails fall back to icons without disturbing the layout.

Desktop widgets retain their declared grid footprints for now; do not introduce
arbitrary resizing as part of this guide. Preserve per-user placement and pins.
On a narrow viewport, offer a readable reflow/list arrangement without silently
rewriting the user's wide-screen layout. Editing has an explicit mode and clear
entry/exit controls; read-only monitoring should not look draggable all the time.

**NAS-07 — Accounts and shared access. MUST.** Users/groups use Linux identities
consistently. Account-level SMB enablement and password-sync state stay in user
Security; folder publication rules stay in Shared folders. Explain effective
access when Unix permissions limit a requested sharing permission. An ordinary
user sees only permitted information/actions. Protected system accounts and the
last administrator show a concrete reason when an operation is disallowed.

Deleting a user preserves the accepted default to remove their home directory;
the short confirmation names that directory and shows the checked option clearly.
Files in shared folders are preserved. Relocating homes first checks blockers,
then shows affected users for confirmation. Do not expose a PID as the only
explanation of a blocking service.

**NAS-08 — Modules are part of one product. MUST.** Module cards remain compact:
icon, name, installed/available version, explicit installation state and actions.
Use a labeled state such as Installed instead of an unexplained dot; retain the
All/Installed filtering model. Opening a card leads to details with the same
actions. Show missing dependencies, required access and compatibility before
installation when they affect the decision. Progress belongs to common tasks.
Uninstall explains whether configuration or user data will be retained. Core and
external modules use the same settings, notifications, translations and error UX.

## 8. Accessibility and localization

**A11Y-01 — Target WCAG 2.2 AA. MUST.** Treat this as the acceptance target for
complete supported workflows, not a compliance claim made by this document.
Automated checks supplement keyboard and assistive-technology testing. Provide
landmarks, meaningful headings, a skip-to-content route, semantic links for
navigation and buttons for actions. Preserve browser zoom. Every control has an
accessible name, role and state. Login supports password managers and paste.
[WCAG 2.2](https://www.w3.org/TR/WCAG22/)

**A11Y-02 — Keyboard and focus. MUST.** All supported tasks work without a mouse.
Tab order follows reading order; focus remains visible and is not hidden by
sticky regions. Our target is full focus visibility, stronger than AA's minimum
“not entirely hidden” requirement. Do not reset focus on polling. Closing or
removing an object moves focus to a logical surviving control. Avoid positive
tabindex and double activation from nested controls.
[W3C: Focus not obscured](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html)

**A11Y-03 — Targets, motion and changing content. MUST.** WCAG AA's target minimum
is 24×24 CSS px with defined exceptions; our 32/40/44px choices are stronger
project defaults. Honor reduced motion: remove decorative animation and give a
static busy cue plus text instead of depending on continuous spinning. Avoid
flashing. Maintain readable names, selection and progress in forced-color modes.
Allow pausing nonessential auto-updating presentation when it distracts, without
stopping the actual background operation or hiding critical conditions.
[W3C: Target size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)

**A11Y-04 — Implement the actual interaction pattern. MUST.** Use a simple nested
list with disclosure buttons unless a real tree's keyboard model is implemented.
For the file tree, arrows navigate/expand/collapse, Home/End reach the boundaries,
and activation is distinct from selection. Use accessible selection semantics and
keep focus distinct from selected rows. Tabs, command menus and dialogs follow
their established patterns. A CSS grid is not automatically an ARIA grid.
[W3C tree view pattern](https://www.w3.org/WAI/ARIA/apg/patterns/treeview/)

**TEXT-01 — Plain, consistent language. MUST.** Use sentence case, short active
verbs and object-specific titles. Avoid implementation identifiers in primary
messages: a user-facing “Share connection” action is not “network.share.save”.
Technical details remain copyable on demand. Reserve “Delete” for deletion,
“Remove from array/sharing” for removing a relationship, “Unmount” for a filesystem
and “Eject” for safe device removal. Avoid calling all of these “Disconnect”.

**TEXT-02 — Translate complete messages. MUST.** English is the default and
fallback; user choice applies across shell and modules. Modules own their
translation namespaces and reuse core action/state terminology. Avoid assembling
sentences from translated fragments. Handle plurals, localized date/time and
number formatting. Keep proper names, paths, addresses and protocol abbreviations
unchanged. Label binary capacity and byte rates accurately; a USB link speed is
not a measured disk transfer rate.

**TEXT-03 — Content must survive real input. MUST.** Test English, Russian and
Ukrainian with long labels, filenames, IPv6 addresses, duplicate display names and
missing readings. Do not assume a fixed percentage of translation expansion is
sufficient. Wrap decision text and error messages; never hide the critical target
or consequence behind ellipsis. Truncated compact names have an accessible full
value and a way to inspect/copy it.

## 9. Shared implementation contract

**SYS-01 — Evolve the existing stack. SHOULD.** Keep React, existing routing/query
integration, Radix primitives, MDI icons and the current module SDK. These
guidelines do not justify replacing the frontend with Carbon, PatternFly or a
second UI library. Borrow verified interaction patterns; implement them through
shared PaNasMs components and scoped module styles.

The shared UI layer should gradually own semantic tokens and these contracts:
IconAction/Tooltip, StatusIndicator, PageHeader, ContextToolbar, ObjectCard,
FormField, ConfirmDialog, DetailsDialog, WaitingSurface, JobProgress,
AsyncContentState and Notification. These are proposed responsibilities, not a
claim that components with those names already exist. Avoid splitting working
components merely to match these suggested names.

**SYS-02 — Modules consume the same contracts. MUST.** A module registers its
routes, named navigation entry, widgets, settings and translations through the
core interfaces. It uses shared focus/overlay/notification behavior and semantic
tokens. Scope CSS to the module; do not globally restyle label, button or heading
elements. Declare relevant capabilities and handle loading, empty, denied, stale
and error states. Do not assume every NAS has a fan, Wi-Fi, SMART or the same disks.

**SYS-03 — UI work must not create background load without a user benefit. MUST.**
Avoid unbounded image/list loading, unnecessary rerenders and repeated polling of
the same data by multiple widgets. Preserve the existing HTTP snapshot/WebSocket
invalidation model. Pause avoidable hidden-view rendering; background jobs remain
server-owned. Directory thumbnails and automatic probes must respect storage
sleep policy. Test responsiveness during active transfers and reconnection, not
only an idle NAS with a small folder.

**SYS-04 — Review and maintain the standard. MUST.** Use the acceptance checklist below
for each changed workflow. Record exceptions by rule ID, rationale, owner and
review condition; do not silently fork a module's behavior. A new shared pattern
is reviewed in both themes and all three languages before other modules adopt it.
Keep this public guideline updated with accepted patterns. Store machine-specific
evidence and delivery records privately; this document tracks desired UI behavior.

## 10. Research basis and deliberate adaptations

Sources below were consulted on **2026-09-21**. W3C defines accessibility criteria;
APG describes interaction patterns. Design systems and UX research inform choices
but do not prove that a particular PaNasMs screen is usable. Confirm the combined
design against the real tasks in the checklist.

| Source | What we take | Boundary |
| --- | --- | --- |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) and its linked Understanding pages | Measurable accessibility target | Not a ready-made visual design or proof of conformance |
| [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/) | Correct interaction semantics for complex controls | Native HTML first; roles alone do not implement behavior |
| [NN/g: Icon usability](https://www.nngroup.com/articles/icon-usability/) | Recognition and the cost of ambiguous icons | Owner's compact toolbars retained; named menus and accessible alternatives added |
| [NN/g: Confirmation dialogs](https://www.nngroup.com/articles/confirmation-dialog/) | Specific consequences and restrained confirmation | Typed confirmation explicitly rejected for this project |
| [KDE HIG](https://develop.kde.org/hig/) | Familiar desktop tasks and progressive complexity | No copying desktop-only navigation/API rules into a web SPA |
| [Carbon notifications](https://carbondesignsystem.com/components/notification/usage/) | Appropriate feedback channels | Our persistent task/event model and compact shell remain |
| [Carbon loading](https://carbondesignsystem.com/patterns/loading-pattern/) | Scope and meaning of waiting indicators | Our scoped overlay and background-job handoff take precedence |
| [GOV.UK error messages](https://design-system.service.gov.uk/components/error-message/) and [summaries](https://design-system.service.gov.uk/components/error-summary/) | Specific, associated errors and preserved input | A single-field dialog need not duplicate an entire page-level summary |
| [Synology storage management](https://www.synology.com/en-global/dsm/7.4/software_spec/storage_management) | Distinct storage layers and object context | Linux capabilities and actual PaNasMs objects determine our hierarchy |

## Review and acceptance checklist

For each changed workflow record the route, version, role, language, theme,
viewport, input method and results. Mark each item Pass, Fail, Not tested or Not
applicable. A screenshot alone does not prove accessibility or backend safety.

- Verify supported tasks, ownership of actions and consistent object identity.
- Check direct URLs, refresh, Back/Forward, empty/error/loading and stale states.
- Check both themes, realistic wallpaper, EN/RU/UK, long names and missing data.
- Check 320, 390, 768, 1024 and 1440px widths, text scaling and page zoom.
- Check keyboard navigation, focus, accessible names and screen-reader behavior.
- Verify contextual actions, compact confirmations, preserved input and recovery.
- Verify folder-policy enforcement and permissions on the server as well as UI.
- Verify task progress, cancellation boundaries and reconnect behavior.
- Verify shared tokens, full-height tabs and restrained elevation.
- Record deviations and untested cases explicitly before claiming conformance.
