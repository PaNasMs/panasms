A multi-select chooses several items from a list: users with access, protocols, groups.

- Markup: `<div class="multi">` holds a `chip` per chosen item, each with a remove button labelled "Remove <name>". The options open as a `menu` of `check` rows.
- The field grows in height as chips wrap; it never scrolls sideways.
- Empty: show a muted "Nothing selected" placeholder. If at least one item is required, say so in the hint and mark the field invalid on Apply.
- On a phone the options open as a bottom sheet with a Done button.
- One shared component for the core and all modules.
