# Site day-path refactor

- Run ID: `2026-08-01-183555-site-day-path`
- Started: 2026-08-01T18:35:55Z
- Seeds: Codex + Claude, read-only design consultation
- Starting commit: `14d4c5c`
- User-approved direction: the online website is the complete learner surface; required learner material currently exposed as Markdown becomes web content; staff/source Markdown leaves learner routes; primary navigation follows Pre-work and Monday through Friday; handouts remain contextual and secondary.
- Deployment: not authorized in this run; validate the repository and local served site only.

## Status

Complete in the working tree. Deployment was not requested or performed.

## Result

- Primary navigation is limited to Pre-work and Monday through Friday; the brand remains the home route.
- The visible path is `PREWORK → B0 → P1 → P2 → P3 → P4 → P5 → P6 → P7 → P8`, with B0–P8 numbered as nine modules.
- The home page and pre-work hub are map-first. Pre-work rolls 62 observable required checks into five visual phases; 17 reference/conditional checks and five optional checks no longer gate READY.
- The detailed install guide keeps the five required phases contiguous, collapses step instructions by default, and places optional tools and troubleshooting in closed lanes after the Monday handoff.
- Visible raw Markdown links were removed or replaced with web pages. Optional handouts are contextual, time-labeled, and return to their owning module.

## Validation

- `node --check site/js/registry.js`
- `node --check site/js/shell.js`
- `node scripts/build-resources.mjs --check`
- `node scripts/verify-resources.mjs` — 0 warnings
- `python3 -m py_compile server.py`
- `python3 .github/scripts/verify-stack-facts.py` — 15 checks, 0 hard failures, 0 warnings
- static document-root requests for the home page, pre-work, setup log, B0, P8, a resource page, JavaScript, and the pre-work SVG — all HTTP 200
- 84/84 checklist IDs preserved; five phase anchors and all local fragments resolve
