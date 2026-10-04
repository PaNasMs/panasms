A field is a label, one input and an optional hint or error line.

- Markup: `<label class="field">Label <input class="input"> <span class="hint">…</span></label>`. Use `select` for a native list and `textarea` for several lines.
- The label is always visible above the input; a placeholder is an example, never the label.
- Error: set `aria-invalid="true"` on the input and add `<span class="error">` that says what to enter, linked with `aria-describedby`. The hint is replaced by the error, not stacked with it.
- Fields are 48px high (`control-lg`) with `radius-pill`; a multi-line field uses `radius-md`.
- Fields always sit on `panel-solid`, also in the translucent themes, so typed text never lies over the wallpaper.
- Disabled fields keep their value visible and explain the reason in the hint.
- Border `line-strong`; hover `ink`; focus a 3px `focus` ring; invalid `danger` border on `danger-bg`.
