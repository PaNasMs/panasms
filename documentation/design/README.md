# PaNasMs design sources

`home/` is the design system of the "Home" look (owner decisions of 2026-10-04,
see section 13 of [the interface design standard](../../docs/ui-design-guidelines.md)).

| Path | What |
| --- | --- |
| `home/README.md` | Brand book: content rules, visual foundations, layout, iconography, translation |
| `home/tokens.json` | Tokens: colours for four themes, type styles, spacing, radii, shadows, sizes |
| `home/components/bundle.css` | Reference stylesheet of the components |
| `home/components/<Name>/README.md` | Guidelines of one component |
| `home/components/<Name>/preview.html` | Static preview; open it next to `tokens` through the design tool, or read it as markup reference |
| `home/functional-map.md` | Inventory of the interface the redesign has to carry |

The shipped implementation lives in `PaNasMs/frontend` (`src/home/`). When the
two differ, the frontend is what users get; fix the design source or the code so
they agree again.
