# PaNasMs Home

The target look of PaNasMs, the web panel of a home NAS. It replaces the current look, which the owner describes as a draft: flat, inconsistent between components, and unusable on a phone. This system is the design reference; it is not yet implemented in `PaNasMs/frontend`. The snapshot of the current look is a separate system, "PaNasMs Design System".

## What it should feel like

A household appliance, not an admin console. Large soft panels, pill-shaped controls, generous hit areas, one warm accent. A person who is not a system administrator must be able to use every page on a phone, including storage and network settings.

## Content

- Name things by what the person recognises: "Sections", "Disks and storage", "Sync tasks". The launcher is "Sections", never "Applications".
- A button is verb plus object: "Delete array", "Add sync task". Never "Yes", "No" or "OK".
- An error says what went wrong and what to do: "Cloud is unreachable; retry later."
- State is always a word, never colour alone: "Healthy", "Degraded", "Failed".
- Sentence case everywhere. Units with a space: `931.5 GiB`, `35 °C`.
- The interface ships in English (default), Russian and Ukrainian. Russian and Ukrainian labels are about a third longer; no layout may depend on an English label fitting.

## Visual foundations

**Themes.** Four: Light, Dark, Light translucent, Dark translucent. Each has its own built-in background (defined in `components/bundle.css`); a wallpaper uploaded by the user replaces it. In the translucent themes `panel`, `inset` and `line` let the background through and panels blur what is behind them.

**Nothing on the bare background.** Because the background can be any picture, text and controls never sit on it. The page title and page actions live in the Page header panel; group headings live inside cards.

**Always opaque.** Dialogs, sheets, menus, tooltips, toasts and form fields use `panel-solid` in every theme.

**Colour roles.** `ink` on `panel` for text; `mute` for secondary text. `accent` (yellow) is a fill for exactly two things: the one primary button of a view and the current section in the taskbar. `second` (blue) is for links, progress, selection and counters. `ok`, `warn`, `danger` each have a text colour and a `-bg` fill. The current item of Section navigation is an `ink` fill with `on-ink` text.

**Type.** Manrope, eight styles from `caption` 12px to `figure` 36px. Body is 15/22 at weight 500; emphasis is weight 700, never italics or colour.

**Shape.** Four radii: `radius-sm` 12px for tags and menu items, `radius-md` 18px for rows and tiles inside a card, `radius-lg` 24px for cards and dialogs, `radius-pill` for buttons, fields and the taskbar. Nested shapes step down one size.

**Space.** Six steps, 4 to 32px. Cards are padded `space-5`; cards in a column are `space-4` apart; page regions `space-5`.

**Size.** Every control is at least `control` 44px high; fields and navigation items `control-lg` 48px.

**Depth.** Panels have no shadow; they separate from the background by fill. Shadows are only for things that float: `shadow-pop` for menus and toasts, `shadow-dialog` for dialogs and sheets.

**States.** Every interactive component defines hover (`hover` overlay), pressed (`press` overlay), keyboard focus (3px `focus` ring), disabled (`disabled` text on `inset`, with the reason in words nearby) and busy (`aria-busy`, spinner in place of the label).

## Layout

- Shell: the Taskbar (top on a computer, bottom on a phone), then the Page header, then content.
- A section with parts uses Section navigation: a 232px rail from 1024px, a switcher that opens a sheet below. One navigation level per page; no tabs.
- Breakpoints: phone below 640px, tablet 640 to 1023px, computer from 1024px.
- The desktop is a grid of Widgets with separate layouts for computer and phone.
- Side gutter `space-5` on a computer, `space-4` on a phone.

## Iconography

Line icons on a 24px grid, 2px stroke, round caps, drawn with `currentColor` (class `icon`, 20px by default). The previews use hand-drawn stand-ins.

The product keeps the `@mdi/js` package. Solid-shape icons use their outline variants (`mdiLockOutline`, `mdiPencilOutline`, `mdiUsbFlashDriveOutline`, …); line glyphs such as check, close, plus, download and upload, and the media controls, stay as they are.

## Translation

Checked with the real Russian strings (see the canvas boards "Settings in Russian").

- The section rail fits the longest Russian label ("Контейнеры и приложения") in two lines at 232px; labels wrap, they are never cut.
- A segmented control with long options ("Тихий / Сбалансированный / Производительный", about 430px) does not fit a phone. Rule: on a phone, or whenever the options do not fit on one line, the same setting is a select.
- Buttons never shrink their text; a row of buttons wraps.

## Open items

- Final artwork for the four theme backgrounds (the current ones are gradients). Owner decision.
- Contrast of `mute` text on translucent panels over real photographs has not been measured.
- Ukrainian strings were not laid out; they are close to Russian in length.
- Not drawn: Files on a phone with a selection, container detail page, user wizard, Wi-Fi network list.
