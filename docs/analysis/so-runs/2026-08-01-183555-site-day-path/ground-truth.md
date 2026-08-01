# Ground-truth manifest

Recorded before implementation against the current working tree.

## Verified architecture

| Concern | Existing source of truth | Verified pattern |
|---|---|---|
| Course order and progress | `site/js/registry.js` | Plain object registry, one local-storage key per checklist, declared required IDs |
| Shared learner navigation | `site/js/shell.js` | `buildNav`, registry-derived day menus, context strips, previous/next plates |
| Contextual handouts | `resources/catalog.json` and `scripts/build-resources.mjs` | Node built-ins only; source fragments generate static pages and module shelves |
| Link validation | `scripts/verify-resources.mjs` | Walks every site HTML file and validates local targets and fragments |
| Hosting | static files plus `server.py` | No framework or package dependency required |

## Runtime facts

- Node: `v22.23.1`
- Python: `3.9.6`
- No package manifest, framework, or new dependency is needed.
- Browser APIs already in use: DOM query/event APIs, `URL`, and `localStorage`.

## Baseline verification

- `node scripts/verify-resources.mjs`: pass, zero warnings.
- `python3 .github/scripts/verify-stack-facts.py`: one pre-existing hard failure because the concurrently edited tree removes `lead/COHORT_PIN.md`; unrelated to this learner-surface refactor.
- The current visible surface contains raw Markdown links across block, pre-work, operator, instrument, pulse, and generated handout pages.
- The current context label denominator is the full registry length, while its numerator counts only keyed entries, producing false labels such as P1 “Block 3 of 11.”
- The current pre-work required list includes conditional `wg-fix` and seven `r-*` recovery checks.

## Implementation choices grounded in existing code

- Extend the current registry rather than introduce a router or framework.
- Preserve existing storage keys and valid check IDs; change required membership, not stored state.
- Extend the existing dependency-free link verifier to prohibit visible Markdown links.
- Change generated handout navigation in the generator, then rebuild; never hand-edit generated resource pages.
- Preserve exact learner commands and file paths shown as code text.
- Per the user’s clarification, do not change repository-serving access rules; visible navigation and links are the boundary.

