A button starts an action; `primary` marks the one main decision of a view and `danger` the one that destroys data.

- Markup: `<button class="button">`. Variants: `primary`, `danger`, `quiet` (outlined, for the least important action in a row), `icon-only`, `large` (page header), `on-wall` (never needed if the page-header rule is followed).
- The consumer provides the label as verb plus object ("Delete array", "Add sync task"). An `icon-only` button needs `aria-label` and a tooltip with the same words.
- One `primary` per view or dialog. Cancel comes before the confirming action. A destructive confirmation uses `danger`, never `primary`.
- Final decisions (Apply, Delete, Cancel, Save) always carry words. Icon-only is for repeated row tools on a computer; on a phone give the action a label or move it into a labelled menu.
- Height is `control` (44px) everywhere, `control-lg` (48px) with `large`. Do not shrink.
- A disabled button keeps its label; say next to it why it is unavailable. While the action runs set `aria-busy="true"`: the label is replaced by a spinner and the width does not change.
- Colours: default `inset` + `ink`; primary `accent` + `on-accent`; danger `danger` + `on-danger`. Hover and pressed add the `hover` and `press` overlays; focus is a 3px `focus` ring.
