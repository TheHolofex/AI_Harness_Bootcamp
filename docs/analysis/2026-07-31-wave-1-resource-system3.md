# Wave 1 resource system — System 3 analysis

Date: 2026-07-31  
Decision owner: course repository  
Scope: the 17 approved Wave 1 module resources plus PC-1

## Phase 0 — problem and evidence

This is not only a writing job. It creates a second learner surface beside the rebuilt block pages, so the main risks are semantic drift, shelfware, staff leakage, and a navigation/build system that collapses when the catalog grows from 18 to roughly 50 handouts.

Evidence checked on disk:

- The course is a static HTML site served unchanged by `server.py`; there is no package manifest or runtime site build.
- `MEMORY.md` makes the block pages the canonical learner surface and names stack facts that override a drafter's memory.
- The existing Resources page is a flat shelf. It includes learner links to staff-oriented source material, so the audience boundary needs repair.
- `site/js/shell.js` understands only root, `blocks/`, and `checklists/` paths. Arbitrarily nested resource pages would resolve navigation incorrectly.
- The two existing handouts have separate Markdown and HTML copies with different lengths and heading counts. No file declares which copy owns the teaching.
- The existing figure family is editable SVG: fixed view boxes, selectable text, restrained paper/red/gold tokens, titles/descriptions, and no scripts.
- There is no shared print contract, resource build, catalog validator, or resource-specific leak/dedup gate.

## Phase 1 — frames and assumptions

Three plausible frames were tested:

1. **A set of pages:** hand-author 18 finished HTML pages and link them.
2. **A small publishing system:** keep one content source and compile the hub, module shelves, pages, and figures into committed static output.
3. **A client-side application:** ship content as data and render the resource experience in JavaScript.

Assumptions made explicit:

- Future maintainers can run Node, but the hosted learner site must not need Node or a client-side framework.
- Learners may print or save pages and may browse with JavaScript unavailable; the prose must be real HTML at rest.
- The module is a useful shelf-sized unit; exposing every handout in the global header would overload it.
- Block concepts require stable anchors so an extension can point to the exact canonical statement.
- “Several figures” means multiple instructional views that earn their place, not decorative pictures.
- Usage is not currently instrumented. Wave promotion therefore needs an explicit facilitator/learner evidence mechanism, not assumed click analytics.
- P5 protection applies to filenames, labels, captions, SVG text, alt text, and links—not only visible paragraphs.
- A generated page is acceptable only when the editable source and generated ownership are unmistakable.

## Phase 2 — fracture findings

Independent reviews converged on these findings:

- **Architecture skeptic:** use a narrow resource-only build; never keep a hand-edited portable copy beside a separately edited web copy. A format choice alone does not prevent conceptual duplication, so keep an internal scope ledger with exact block anchors and prohibited restatements.
- **Accessibility/front-end review:** put the hub plus module shelves in the Resources disclosure; keep handout titles out of the global menu. Use breadcrumbs, contents, module-local navigation, visible captions, figure transcripts, full-size figure links, coarse-pointer targets, reduced-motion handling, and a real print stylesheet.
- **Curriculum-library view:** the block page owns doctrine; the handout must provide a new case, instrument, practice, evidence artifact, or transfer move. “More explanation” is not enough to publish.
- **Build/visual view:** use one public catalog and deterministic, editable SVG templates. Validate links, fragments, IDs, alt text, XML, geometry, staff paths, and orphaned output after generation.
- **Minimal-maintainer view:** do not replace the static site or Python host. The resource compiler should be removable without disturbing the course spine.

## Phase 3 — synthesis

The useful metaphor is a field library with an acceptance rig:

- The **catalog** is the card index.
- Each **HTML manuscript fragment** is the sole editable body.
- The **compiler** binds manuscripts into static learner pages and module shelves.
- The **figure kit** turns small, reviewable specifications into editable SVG plates in the existing family grammar.
- The **acceptance rig** rejects broken links, leaked staff material, malformed figures, duplicated teaching, and unprintable artifacts.

HTML fragments are chosen over Markdown for this repository. Both independent reviews preferred Markdown if a pinned CommonMark implementation already existed, but none exists on disk and adding a package graph solely for 18 pages would enlarge the course's maintenance surface. A semantic HTML fragment preserves the one-source rule, matches the current canonical site format, and needs only Node built-ins. The decision is reversible because the catalog, output paths, and page contract do not depend on the manuscript syntax.

Resource information architecture:

```text
Resources
├── Hub
├── Pre-work
├── P1 … P8
└── Pocket card
    └── each module shelf lists only its own resources
```

The top disclosure exposes shelves, not all titles. Every handout has two inbound routes: its module shelf and a contextual “Go deeper” link from the owning block or pre-work page. The hub displays `Use when`, time, and produced artifact before a learner opens a page.

## Phase 4 — decision audit

### Selected design

- `resources/catalog.json` — public learner metadata only.
- `resources/handouts/<module>/<slug>.html` — sole editable body fragment.
- `resources/figures/<module>/<resource-id>.json` — figure specifications.
- `resources/scopes.json` — internal canonical owner, collision IDs, novel work, and prohibited restatements; never shipped.
- `scripts/build-resources.mjs` — committed static hub, module pages, handouts, resource nav data, and SVGs.
- `scripts/verify-resources.mjs` — portfolio acceptance checks.
- `site/resources.html` — stable hub URL.
- `site/resources/<module>/index.html` and `<slug>.html` — generated shelves and handouts.
- `site/assets/resources/<module>/*.svg` — ordinary editable SVG output.

### Rejected alternatives

- **Manual complete HTML pages:** lowest startup cost, but repeats chrome and metadata 18 times and recreates the existing dual-copy drift.
- **Runtime JavaScript prose rendering:** worsens print, no-JS use, deep linking, inspection, and audience-data leakage.
- **Nested flyout of every title:** does not scale to 50 items and adds keyboard, touch, and magnification failure modes.
- **Image generation:** conflicts with the established editable figure grammar and makes label correction non-deterministic.
- **A new docs framework:** solves a much larger problem than this repository has and changes the hosting/runtime contract unnecessarily.

### Bias and failure check

- Status-quo bias favors hand-edited HTML; abstraction bias favors a new toolchain. A dependency-free, resource-only compiler is the smallest reversible middle.
- “More content is better” is rejected. Wave 1 publication requires practice and an observable artifact; later waves require actual usage evidence.
- Click counts are not assumed. Recommended evidence is a facilitator contextual-use tally, one cohort exit item per resource used, and transfer-artifact completion.
- A validator cannot prove pedagogical distinctness. Final cross-module semantic review remains human/agent judgment.

Self-audit: problem definition 5/5; assumption validity 4/5; perspective diversity 5/5; creative exploration 4/5; bias awareness 5/5.

## Phase 5 — implementation manifest (ground truth)

### Interfaces and facts verified

- Runtime: Node `v22.23.1`; generator may use only `node:fs`, `node:path`, `node:url`, and other Node built-ins.
- Host: `server.py` serves committed files and blocks named staff/answer-key paths; no runtime build hook will be added.
- Front-end: vanilla browser JavaScript; existing pages load `site/js/registry.js` then `site/js/shell.js`.
- XML check: `/usr/bin/xmllint` is present.
- HTML check: `/usr/bin/tidy` is present.
- Source-of-truth facts: `MEMORY.md`, the owning block/pre-work page, operator instruments, and learner-visible mission files. A draft may not override them.

### Inputs and outputs

- Input catalog entries require: ID, module, order, slug, title, summary, `useWhen`, time, artifact, prerequisite, canonical path/anchor, related IDs, source, figures, status, and wave.
- Every body fragment must include the full learning arc: orientation, mechanism beyond the block page, worked example, failure injection, guided practice, evidence artifact, self-check, transfer move, and primary/authoritative sources.
- Every figure spec requires a unique ID, one supported layout, title, description/transcript, caption, and layout data.
- Generated pages carry a DO-NOT-EDIT marker and explicit body metadata.

### Acceptance commands

```bash
node --check scripts/build-resources.mjs
node --check scripts/verify-resources.mjs
node scripts/build-resources.mjs
node scripts/verify-resources.mjs
git diff --exit-code -- site/resources.html site/resources site/assets/resources
```

The verifier must additionally run or enforce:

- claims-vs-disk link and anchor audit, including case-sensitive paths;
- staff-leak and making-of grep across sources, catalog, rendered HTML, SVG text, titles, descriptions, captions, and alt text;
- P5 fresh-example rail with no intake-item identities or hints;
- HTML parse, duplicate-ID, heading, alt, and orphan checks;
- SVG XML, viewBox, ID, minimum-type, and geometry checks;
- reciprocal related-resource and contextual inbound-link checks;
- exact one-page print verification for PC-1;
- final cross-module semantic dedup review.

## Phase 6 — recommendation

Build only Wave 1 plus PC-1. Establish the catalog/compiler/verification rails first, then draft resources in maximum-safe parallelism. Publish only pages that survive a source-grounded content review, a fresh pedagogical review, the deterministic acceptance rig, a desktop/mobile/print inspection, and one portfolio-wide dedup pass.
