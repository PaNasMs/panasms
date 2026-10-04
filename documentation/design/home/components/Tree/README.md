A tree shows nested things: folders in the folder picker, devices with their partitions and file systems in Storage.

- Markup: `<div class="tree" role="tree">` with `<button class="node" style="--lvl:N">` rows; an icon, the name, and an optional `.meta` second line. The selected node has `aria-selected="true"` (ink fill).
- Folder picker = this tree in a dialog, with the chosen path under it, "Create folder", and Cancel / "Select folder". One picker for the core, Files and Cloud Sync.
- Unavailable nodes stay visible with `aria-disabled="true"` and a reason in the second line.
- In Storage, selecting a node shows the Selection bar with the actions valid for that kind of node.
- Indent is 22px per level; rows are 44px. On a phone the picker is a full-height sheet.
