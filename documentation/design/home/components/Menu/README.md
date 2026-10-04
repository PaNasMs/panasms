A menu lists the actions of one object; a tooltip names an icon-only control.

- Markup: `<div class="menu" role="menu">` with `<button role="menuitem">` rows, each an icon plus verb-and-object label; `<hr>` separates groups; the destructive item is last with `danger`.
- Menus, tooltips, dialogs and sheets are always opaque (`panel-solid`), in every theme.
- On a phone a menu opens as a bottom sheet with the same rows, 52px high.
- An unavailable item stays in the menu, disabled, so the list does not jump.
- Tooltip text equals the control's `aria-label`. Never put information in a tooltip that is not available elsewhere.
