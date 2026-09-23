# Modal dialog conformance pass

2026-09-23 · PaNasMs core and installed module UI

Scope: all 36 production `DialogContent` call sites in this workspace, including
core features and the Files, Terminal and Cloud Sync modules. The
[interface design standard](../docs/ui-design-guidelines.md) is the normative specification.
This report distinguishes implementation review from live destructive-operation tests.

## Changes by area

| Area | Dialogs reviewed | Corrections |
| --- | --- | --- |
| Shared UI | Confirmation, unsaved edits, folder selection | Explicit layout slots; one internal close glyph; fixed header/footer and scrolling body; safe focus; in-place discard decision; nested picker replaces visible parent while retaining its draft |
| Storage | SMART, generic operation forms/reviews, eject, damaged filesystem, file collision | Shared variants; stable SMART frame and per-tab scroll; icon toolbar retained; confirmations preserve server preview and fingerprints; automatic media prompt waits while another dialog is open |
| Network | Interface edit/details, sharing wizard/actions, AP settings, Wi-Fi selection/confirmation, rollback countdown | Common heading/footer; AP final actions use words; controlled dirty state; Wi-Fi selection and confirmation do not overlap; closing countdown does not accept configuration and explicitly leaves rollback running |
| Settings/modules | Home migration/blockers, HTTP port confirmation, module install/modify, repository sources, OS update | Shared close and sizes; accepted module/update jobs release their modal; source-list loading remains dismissible |
| Identity/power | Session termination, Google consent/link/unlink, grant revocation, power confirmation | Shared compact/form layout, safe confirmation focus and unboxed close; authentication/authorization remains unchanged |
| Files module | Destination selection, preview, batch deletion, permissions | Explicit layout; preview loading is dismissible; deletion keeps Trash/Delete/Cancel; permissions use shared discard state instead of a second dialog; footer submit buttons stay associated with their form |
| Terminal module | Stop-all confirmation | Shared compact dialog and close; preserve browser-local session scope |
| Cloud Sync module | Connection/sync wizard, removal confirmation | Shared heading/footer and close; selected folders count as unsaved edits; picker return retains wizard values |
| Toasts | Local and server event popups | Shared 20px close glyph centered on top-right corner, half outside on both axes; 44px hit target and unclipped focus ring; dismissal remains local to the toast |

## Shared implementation

`frontend/src/shared/waiting.tsx` owns close appearance, focus intent, dirty dismissal,
waiting and nested-view visibility. A nested Radix root is retained for primitive
focus management, but its parent panel and backdrop are hidden while the child is
visible; returning restores the original component state. Unsaved confirmation
uses the existing content container. This does not flatten all workflows into a
new global dialog state machine.

New call sites provide `header`, optional `footer`, `variant`, `intent` and, for
custom editors, `dirty`. Legacy child classification remains for previously
published modules. Core supplies the runtime; module SDK declarations and README
now describe the contract. The workspace module build also resolves the existing
external-connections SDK entry used by Cloud Sync.

## Verification

- Core TypeScript and production build passed.
- TypeScript and production UI builds for Files, Terminal and Cloud Sync passed.
- Existing unit suite: 51 passed.
- New `frontend/tests/dialogs-browser.mjs` checks actual shared components in Chrome:
  fixed header during scroll, one visible nested dialog/backdrop, parent draft
  preservation, keep/discard and focus return, busy Escape blocking and recovery,
  safe initial focus and outside-click protection, return to manual (non-Trigger)
  openers, toast icon geometry, and
  320/390/768/1024 CSS px layouts.
- Theme screenshots reviewed; new tests do not submit real NAS operations.
- Live NAS browser: SMART attributes/results, review-only SMART operation and
  return to the selected results tab; shared-folder form and nested directory picker; Files permission editor and
  Cloud Sync wizard opened and dismissed without saving.
- Disk tests, shutdown, reboot, formatting, network changes and deletions were not
  executed to validate presentation. This is not certification of every hardware,
  screen-reader, mobile-keyboard or zoom combination in the full acceptance matrix.

## Delivery

Core and all three module UI assets were updated together, with prior assets backed
up on the test NAS. Machine-specific deployment records remain private. This pass does not publish signed module releases or a registry
update. The module/core release process must use the updated SDK declarations and
compatible core before distributing these module frontends independently.

Run the browser regression with a local Vite server on port 5173, then
`npm run test:dialogs` in `frontend`. Set `DIALOG_TEST_URL` for a different local port.
