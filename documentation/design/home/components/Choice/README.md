Choice controls: checkbox for independent options, radio for one of several, switch for a setting that applies at once, segmented control for two to four short values of one setting.

- Markup: `<label class="check"><input type="checkbox"> Label</label>`; radio the same with `type="radio"`; switch `<input class="switch" type="checkbox" role="switch">` inside the same label; segmented `<div class="segmented" role="radiogroup">` with `<button role="radio" aria-checked>`.
- A switch changes the system immediately; if the change needs Apply, use a checkbox.
- The segmented control is a form control for a value. It is NOT navigation between parts of a section: that is always Section navigation.
- More than four options or long labels: use a select.
- The whole label row is the hit area and is at least 44px high.
