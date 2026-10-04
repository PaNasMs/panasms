The empty state says why a place is empty and what to do next; the waiting state covers a surface while its operation runs.

- Markup: `<div class="empty">` with an icon, a heading, one sentence and at most one button.
- Three cases: first use (explain the feature and offer the first action, `primary`), nothing matches a filter (say so and offer to clear it), nothing yet (say when content will appear, no button).
- Do not use a Notice as an empty state.
- Waiting: wrap the surface in `.waiting` and add `.waiting-veil` with a spinner and a verb ("Applying…"). The content stays visible underneath so the page does not jump.
