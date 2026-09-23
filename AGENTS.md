# PaNasMs project instructions

## Interface design and implementation

- Before designing, implementing or reviewing any interface in the core or a
  module, read [the PaNasMs interface design standard](docs/ui-design-guidelines.md)
  and follow its applicable requirements and acceptance checklists. It is the
  single source of truth for UI/UX, including dialogs and toast notifications.
- This applies to pages, settings, profile, widgets, navigation, forms, tables,
  dialogs, pickers, notifications and background-task presentation in all modules.
- Reuse shared components, semantic tokens and module SDK contracts. Fix shared
  behavior in the shared layer rather than creating per-module visual/interaction
  variants. Consult the guide before extending a shared component.
- Apply the guide's design workflow before coding. Verify the changed states and
  transitions; report untested cases honestly. A build or screenshot alone does
  not establish accessibility or complete conformance.
- Current explicit user instructions take precedence. When an accepted design
  decision changes a rule, update the canonical standard and affected references.
  Record other exceptions by rule ID, rationale, owner and review condition.
- Public documentation and code/review artifacts use English. UI changes must
  support English (default/fallback), Russian and Ukrainian and both themes.
- In a standalone component checkout, read the same published standard at
  https://github.com/PaNasMs/panasms/blob/main/docs/ui-design-guidelines.md.
  Do not maintain a competing copy of the rules in a component repository.

## Documentation boundary

- `docs/ui-design-guidelines.md` is explicitly public in the main repository.
  Other local `docs/` contents are private plans, research and working records;
  never add the directory wholesale or publish its nested Git repository.
- Keep session notes and implementation/deployment history outside `AGENTS.md`.
