# PaNasMs modal dialog guidelines

The normative requirements now live in the [PaNasMs interface design standard](../docs/ui-design-guidelines.md#10-modal-dialogs),
including [MOD-03: shared close control and toast placement](../docs/ui-design-guidelines.md#mod-03)
and the [acceptance checklist](../docs/ui-design-guidelines.md#dialog-and-toast-acceptance).
Use the unified standard for design, implementation and review. This page preserves
existing links and the research assessment; it is not a second specification.

## Research notes

Reviewed on 2026-09-23. These are design opinions, not accessibility standards.
Descriptions below are concise assessments; the requirements in the unified standard are our project
specification, informed also by prior owner decisions and primary references.

### Habr article

[Andrey Nasonov: Modal window best practices](https://habr.com/ru/articles/693272/)
provides a useful anatomy and highlights visual stability. The owner initially
selected its external close concept, then superseded that choice with a uniform
internal close icon for dialogs and an overlapping corner icon for toasts. Do not copy its unrestricted
width, screen-edge scrolling or fixed footer geometry. A close control must remain
usable at zoom, and our bounded data dialogs need a body scroller. Its distinction
between “modal” and “dialog” is author terminology, not our component taxonomy.

### Habr discussion

[Article comments](https://habr.com/ru/articles/693272/comments/) show 12 entries;
one is removed and cannot be evaluated. Assessment of the visible discussions:

| Contribution | Decision |
| --- | --- |
| little-brother: scroll between fixed header/footer | Useful; matches our details/forms workflow. |
| Maevv: browser edge is not necessarily screen edge | Useful counterexample to an unconditional edge-scroll rule. |
| Kolobok12309: numerical choices lack justification | Useful; distinguish project tokens from standards. |
| Author: sizes reflect personal preference | Useful qualification; no mandatory 80px grid. |
| ilya_kochetov: distinguish rationale from a design example | Useful review criterion, not an implementation requirement by itself. |
| Semigradsky / author: mandatory input and closing | Keep an exit; enforce access server-side. A separate page alone is not security. |
| evgeniyPP: avoid complex modal workflows | Useful warning, not a blanket ban on tables or small wizards. |
| Author: reusable implementation avoids repeated effort | Useful engineering direction; reuse does not prove usability. |
| Personal remarks and debate about effort | No actionable UI requirement. |

### Medium article and responses

[Knopyaro's translation of Nick Babich](https://medium.com/nuances-of-programming/советы-по-созданию-правильных-модальных-окон-e0a05794b0c2)
reinforces restrained interruption and understandable actions. The live Responses
panel was opened: it reported **no responses** at review time. There are therefore
no Medium comments to endorse or reject.

Reject a universal 25% area limit, two-button maximum and no-scroll rule. They
conflict with our three-way file decisions, SMART inspection and small screens.
The recommendation to keep waiting in a button does not supersede our approved
translucent waiting layer. Avoiding nested editors remains useful; implement
picker and confirmation steps within one shell. The Medium article's section 4 heading
is inconsistent with its body; follow the rationale, not that isolated heading.

### Additional primary references

[IBM Carbon modal usage](https://carbondesignsystem.com/components/modal/usage/)
supports distinct layout regions, content-sensitive sizes and a scrollable body.
We do not adopt all of its defaults: confirmations focus the safe action, and
our dialog close uses a uniform unboxed icon inside the header. WAI-ARIA and WCAG links in the standard’s MOD-03/08 provide the
accessibility basis. Our chosen pixel sizes, top anchoring and color token remain
project choices requiring real UI validation.
