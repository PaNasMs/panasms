An object card shows one thing the person manages — a disk, a network interface, a shared folder, a module — with its state and key figures.

- Markup: `<article class="object-card">`, or `<button class="object-card" aria-pressed>` when the card can be selected. Parts: `.top` (type tag left, state tag right), `.name`, `.big` (one or two key figures), a muted line with the address.
- States: `warn` and `danger` change the fill and always come with a state tag in words. Selected has a `second` outline.
- Object cards sit inside a `card` that names the group (an array, "Other disks").
- Actions: on a computer up to two icon buttons with tooltips in `.top`; on a phone the whole card opens its detail sheet where actions have labels.
- Same structure for every object type; do not invent per-module card layouts.
