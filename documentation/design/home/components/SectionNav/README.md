Section navigation is the only component for moving between the parts of one section. It replaces both the top tabs and the left settings list of the old interface.

- Markup: `<div class="section-layout">` holds `<nav class="section-nav">` and the content. Each item is `<a>` with an icon, `.label` and an optional `.count` or state `dot`; the current one has `aria-current="page"`.
- From 1024px: a rail on the left, 232px wide, as high as its items. Below 1024px: a `section-switcher` button under the page header showing the current item and "3 of 7"; it opens a bottom sheet with the same items.
- Objects (sync tasks, containers): add `objects` to the nav and the layout (264px). Items get a second line `.sub` with the state and a state dot. A `button` at the end of the list creates a new object.
- `.group` labels and `<hr>` split a long list; module-provided items go under their own group.
- One level per page. No tabs inside a part: split it into cards on the same page, a disclosure group, or a separate detail page with a Back link and its own navigation.
- The current item is an `ink` fill with `on-ink` text. The yellow `accent` is reserved for the current section in the taskbar.
- Works the same for two items and for twenty; never switch to another pattern because the list is short.
