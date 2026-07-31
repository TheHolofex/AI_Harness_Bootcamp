# AI Harness Bootcamp — IA & Navigation Spec (handoff)

Companion to the three hi-fi mockups: `Home — Learner Dashboard`, `Block Page — P2 Merged`, `Pre-work — Hub`.
Visual system is unchanged (existing `course.css` / `checklist.css` tokens and components). This spec covers structure only.

## 1. Principles

- One student path: **Home → Pre-work → today's block → next block**. Everything else is reference.
- The site always answers three questions above the fold: where am I, what do I do now, what comes next.
- Progress is the existing localStorage checklist state — no accounts, no server.
- Lead/staff pages stay on the same site, zoned quietly (nav tail + home footer zone), never mixed into the student path.
- One common track. Remove all track-picking UI and `<track>` path segments from learner pages.

## 2. Sitemap (target)

```
/                      Home = learner dashboard
/prework/              Pre-work hub (status panel + 3 stages)
  /prework/keys        Your API keys (reference)
  /prework/install     Install checklist (79 steps, ahb-prework-install)
/blocks/b0 … p8        9 block pages, each MERGED with its checklist
/resources/            Hub: pulse guide, prompt tips, velocity paradox, repo docs
/lead/                 Lead hub: operate-along, case talks, operator pack, instruments
```

- `week.html` is retired; the home journey board replaces it (redirect week → /).
- `checklists/*` pages are retired; each block page absorbs its checklist (redirect to `#mission` anchor). Keep the same storage keys so existing student progress survives.
- `pulse.html`, `operator.html`, `instruments.html` move under Resources/Lead as appropriate; URLs may stay, nav placement changes.

## 3. Navigation shell (every page)

Header (sticky, 56px, paper, hairline bottom):
- Brand lockup left (red disc + STARZL/ENTERPRISES).
- Primary: `Home · Pre-work · Mon · Tue · Wed · Thu · Fri` — day dropdowns list that day's blocks with status dot (● done-tint / ● red current / ○ ahead), AM/PM tag. Current page = red underline (`inset 0 -2px 0 var(--mark)`).
- Hairline divider, then quiet tail: `Resources · Lead` (muted ink, smaller weight).
- Mobile (<560px): same order, nav wraps below brand; dropdowns become full-width panels.

Context strip (block + pre-work pages, under header): `← prev block | DAY · BLOCK n of 11 | next block →` on `--paper-warm`.

Footer: unchanged, plus home page gets the dashed "For the lead & staff" zone above it.

## 4. Wayfinding components

- **"You are here" panel** (home hero, right column): current block eyebrow + title, red progress bar, `n / total steps · %`, primary CTA "Continue where you left off" / "Start this block". Current block = first block whose checklist is incomplete, in order INSTALL → B0 → P1 → … → P8.
- **Journey board** (home): 6 columns — Pre-work, Mon (Foundations), Tue (Craft + verdict), Wed (Knowledge), Thu (Autonomy), Fri (Transfer). Each cell: status dot, `CODE · name`, slot + tool meta. **Completed cells get bg `#F4F8F4`**; current cell bg `#FDF6F0` (also tints its column header). Legend row above the board.
- **Sticky on-page nav** (block pages): `On this page · Orientation · Mission n/n · Operator pulse n/n · If you get stuck` + mini progress bar right. Sits below the header (top: 56px).
- **Prev/next footer plate** (block + pre-work pages): 3-cell hairline grid — prev block / Week map (home `#journey`) / next block.
- **Status panel** (pre-work hub): same pattern as home panel, keyed to `ahb-prework-install` (79 steps).

## 5. Progress model (unchanged storage, new surfacing)

- Keys: `ahb-prework-install`, `ahb-checklist-b0` … `ahb-checklist-p8`. Value: `{ "<check-id>": true, "_updated": ISO }`.
- `stretch-*` ids never count toward required totals (existing rule — keep).
- Home + nav read all keys on load; block pages write on toggle. Same-tab updates re-render; cross-page consistency comes free via load-time reads.
- Block complete = all required ids true. No dates, no cohort clock.
- **Block pages own their id sets and totals.** Home (and any other reader) must count against the block's declared id list — never `Object.keys(storage)` — so stale ids from removed steps (e.g. the deleted `p2-track`) can't inflate counts. Keep one shared registry (block code → key, ids[], total) that both home and block pages import.

## 6. Page patterns

**Home (dashboard):** field hero (eyebrow / H1 / lede / 2 buttons) + You-are-here panel → Your journey board → New here? 3 moves (keys · install · Monday) → Shape of a day (4-cell meta strip) → What "done" means → lead/staff dashed zone.

**Block page (merged):** context strip → eyebrow / H1 / lede → meta-grid (Day · Block · Time · Tools · Your progress) → red rule → sticky page nav → Orientation (2-col: why/leave-with/before-you-start beside lead-box + case-talk callout) → **Run of exercise** = checkable items (border-left + num disc turn green `#2F6B3A`, bg `#F7FBF7`, title strikethrough when done) → **Operator pulse** = 6 checkable items, identical on every block → Pass bar + If stuck (2-col) → prev/next plate. Checklist ids/keys unchanged from current site.

**Pre-work hub:** context strip → 2-col header (title/lede/why beside status panel) → red rule → "Work these in order" 3 stage cards (top border + bg reflect state: done green-tint, in-progress red-tint) → API-keys + twin-engine callouts (2-col) → Done means + Setup log/Monday (2-col) → Stack table → Traps grid (2-col cards) → prev/next plate.

## 7. Copy rules on wayfinding chrome

- Eyebrows/labels: tracked uppercase, `DAY · CODE` format ("Tuesday AM · P2").
- CTAs name the action and destination: "Continue the install checklist", "Start this block" — never "Learn more".
- Status vocabulary: done / you are here / ahead; steps as `n / total · %` in mono.
- Body stays guide-beside (complete sentences, purpose first). No emoji, no exclamation marks.

## 8. Out of scope / kept as-is

- Password gate flow, `server.py`, hosting.
- All teaching content and checklist step text (except deleted track-picking steps).
- Lead-page internals; `resources.html` internals (nav placement only).
