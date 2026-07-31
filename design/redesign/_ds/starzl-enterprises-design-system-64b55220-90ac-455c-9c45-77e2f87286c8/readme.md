# Starzl Enterprises Design System

**Starzl Enterprises** is a specialized defense contractor: spectral operations (electromagnetic warfare / RF), adversarial AI, and operator training & development. HQ Boulder, CO. Contact: inquiries@starzl.com. Founder/PI: Ravi Starzl, PhD.

Three product lines:

1. **Quicksilver Edge & Spectrum** — "the IQ data fabric." Ultra-low-SWaP IQ compression (8×–42× perceptually lossless, ~750× mission-tuned), emitter signature extraction & classification, tactical quantum-resistant encryption (AES-CPE), alt-PNT (GC3 Sentry), jam-resistant transport (Bifrost), sensor-fleet orchestration (Odin). Tagline: **"The Spectral High Ground."**
2. **Adversarial AI & Mission Assurance** — Automated Knowledge Acquisition System, Skill Realignment Suite, Specialized Offensive AI. "Mission-Bound Autonomy" — operator review, provenance, approval throughout.
3. **Operator Development** — AI red-team boot camps, the **Campus Martius** simulation range, targeted red-team engagements.

## Surfaces in this system

| Surface | Look | Tokens | Where |
|---|---|---|---|
| **Marketing website** (starzl.com) | Sand/gold/red "field manual" editorial | `--sand`, `--ink`, `--gold`, `--red-2`… | `css/starzl-site.css`, `components/site/`, `ui_kits/website/` |
| **SENT Ops Dashboard** (internal ops workspace) | Warm "dust" palette, serif + small-caps + mono | `--sent-*` | `ui_kits/sent_ops/`, `components/sent/` |
| **Quicksilver briefing deck** | Dark `#141210` + paper `#ECE7DC`, Arial + Courier New | `--deck-*` | `slides/` |

All three share one family DNA: warm parchment neutrals, a single red/copper accent, monospace labels, hairline borders, **zero corner rounding**, no drop shadows.

## Sources

- **Codebase (mounted, read-only):** `SE_Website/` — `public/*.html` + `public/site.css` (marketing site, ground truth for the website look); `dashboard_ui/design_handoff_sent_ops_dashboard/` (SENT Ops Dashboard hi-fi handoff: 399-line README + runnable React prototype under `design/`); `ops/` (Vite stub, no styles yet); `public/assets/` (30+ brand images, `public/assets/brand/` logo suite).
- **GitHub:** https://github.com/TheHolofex/SE_Website — same website source; explore it for pages not fully mirrored here (`capabilities.html`, `products.html`, `rf-systems.html`, `ai-security.html`, `mission-software.html`, `operator-development.html`, `portfolio.html`, `contact.html`, `dashboard.html`). Readers with access should browse it to go deeper.
- **Uploads:** `uploads/QuicksilverOverview_SENT_June_20262-3.pptx` / `.pdf` — 17-slide Quicksilver briefing deck (June 2026). Extracted text: `research/quicksilver-deck-text.md`; extracted media: `research/deck-media/`.

---

## CONTENT FUNDAMENTALS

**Voice: military-first, declarative, evidence-led.** Short imperative headlines; claims immediately backed by a mechanism or a number.

- **Headlines are commands or verdicts, uppercase by CSS:** "Hold the signal path." · "Performance must survive contact." · "Build for advantage. Prove under pressure." · "The Spectral High Ground." Often end with a period, even as fragments.
- **"We" for the company, third person for the buyer** ("partners size the next step…", "operators build the skills…"). Direct "you" is rare. The deck uses "the commander," "the operator," "the adversary."
- **Casing system:** sentence case in prose; `text-transform:uppercase` handles display type. Mono labels/eyebrows/buttons are ALWAYS uppercase with wide tracking. Product names capitalized: Quicksilver, Odin, Bifrost, Heimdalla, GC3 Sentry, Campus Martius, SENT.
- **Numbers do the persuading:** "8x-42x Perceptually Lossless Compression Ratio", "13 m CEP50", "0 GPS satellites in the loop", "< 1 s spoof detection", "95.2%". Stats get mono type + small-caps key.
- **Em-dash appositive is the house sentence shape:** "Quicksilver — Starzl Enterprises' IQ data fabric — moves far more signal data…" Also "·" middots as separators in data lines ("0.919 top-1 · 0.997 top-5").
- **Restraint vocabulary:** "authorized", "bounded", "under operator review", "provenance", "validated in operational exercises". Never hype words; never exclamation marks; **no emoji anywhere**.
- **CTAs are institutional:** "Request Briefing", "Review Capabilities", "Review Products", "Contact Starzl" — never "Learn more" or "Get started".
- **Status verdicts, one word:** Validated · Completed · Delivered · Pending · In test.
- Slide kickers: small-caps mono ("PREPARED BY", "KEY TAKEAWAY", "WHY SPECTRUM DOMINANCE MATTERS"); running footer "Quicksilver – The Spectral High Ground".
- SENT dashboard copy is terse ops-room register: "Operations", "Members & Access", "Q3 2026 · Cycle 14", timestamps "12m ago", IDs "OP-1142".

## VISUAL FOUNDATIONS

**Overall vibe:** a declassified field manual / private operations room. Warm parchment + near-black, one red accent, mono machine-labels against big grotesk display type. Everything sharp, bordered, gridded, slightly grainy.

- **Color:** page is `--sand #EDE3C8`; alternating sections `--sand-3`; dark sections `--black-2 #17110C`. Text ink `#17120D`, secondary `#302719`, muted `#655337`. Accents: `--red-2 #D33A2C` (primary CTA, brand dot, list squares), `--red #B43A2F` (kickers, hovers), `--gold #A58650` / `--gold-2 #C8A96A` (labels, outlines, borders on dark). Olive `#4F5634` and steel `#2D3030` exist but are sparse. Max 2 background colors per composition (sand + black).
- **Type:** three-font system — **Space Grotesk** 700/uppercase for display (hero 76px/0.95, section h2 48px/1.02, card h3 28px/1.05); **Inter** for body (16px/1.55, card copy 14px); **Space Mono** for every label, button, metric, nav item (9–13px, tracking 0.1–0.18em, uppercase). Letter-spacing on display type is 0.
- **Backgrounds & imagery:** full-bleed photographic heroes behind double gradient scrims (`90deg` + `0deg` dark-brown fades); imagery is warm, desaturated, golden-hour military/ops photography (desert ops, RF hardware, orbital meshes, briefing rooms). Images sit on `--black` and use `object-fit:cover` inside hairline-bordered frames.
- **Grain:** fixed full-viewport fractal-noise overlay, `opacity:0.08`, `mix-blend-mode:multiply` on the website (`.starzl-site::before`); SENT uses the same trick at 0.5/0.35 via its Backdrop component.
- **Borders & cards:** 1px hairlines carry ALL hierarchy — `--line #C8B78A` on light, `rgba(200,169,106,0.28)` on dark. Cards = hairline border + translucent fill `rgba(248,242,222,0.72)` + 18px padding. **No drop shadows anywhere** (sole exceptions: the glowing brand dot, SENT's pulsing "ping" indicators).
- **Corner radii: 0.** Everything is square (SENT allows 2px/4px; its pills/avatars are the only 999px rounds).
- **Metrics/stat cells:** bordered grid cells (border-top + border-left on container, border-right/bottom per cell) with mono small-caps key + 28px Space Mono 700 value.
- **Buttons:** rectangular, 46px min-height, mono 11px/700/uppercase/0.16em. Ghost (gold outline) default; `.primary` red fill; `.dark` black fill. Hover swaps border+text to red (ghost) or border to gold (filled). No transforms, no shrink on press.
- **Hover states:** color/border swaps at 0.12s; card borders turn red (`.offering-card:hover{border-color:var(--red)}`); SENT rows lift background ~3.5% toward fg. Never opacity fades, never scale.
- **Animation:** almost none. Sticky header, smooth scroll, `prefers-reduced-motion` respected. SENT adds slow orbital-ring rotations (90–200s) and 2.4s ping pulses.
- **Layout:** 1280px content / 1440px nav max-widths; 82px section padding; CSS-grid card grids (2–5 cols, 16px gap); section headers are 2-col (title left, muted lede right) over a hairline; ledger/definition rows are label-left grids. Sticky dark header 68px.
- **Transparency & blur:** translucent card fills over sand; SENT topbar uses `backdrop-filter:blur(6px)`. Website uses no blur.
- **Forms:** square inputs on `--sand-2`, hairline borders, mono uppercase labels.

## ICONOGRAPHY

**There is no icon font and no third-party icon set anywhere in the sources.** The brand is deliberately icon-poor:

- **Geometric primitives as marks:** the glowing 9px red `brand-dot` circle; 5×5px red squares as list bullets (`.plain-list`); SENT's 8×8 rotated-45° diamond status pills and 3×10px priority bars.
- **Unicode as UI glyphs:** ">" for card-link arrows, "·" separators, "—" em-dashes, "×" close. No emoji, ever.
- **SENT custom inline SVGs:** `BrandMark` (SENT seal) and 9 abstract 22×22 `Sigil` glyphs (all/mine/review/archive/diamond/council/ring/square/tri) live inline in `ui_kits/sent_ops/components.jsx` — copy from there, don't redraw.
- **Logo suite** (copied to `assets/brand/`): primary lockup (red dot + "STARZL ENTERPRISES" in mono), `-light` variants for light backgrounds, `blocks-fullheight` stacked block mark, `morse-s` S-in-morse mark, `morse-squarebox-chamfer` badge. Deck title-slide lockup: `assets/brand/starzl-deck-lockup.png`.
- **Diagrams over icons:** the deck uses full illustrated figures (`assets/images/quicksilver-l6-l1-stack-architecture.png`, `assets/images/deck-ew-pyramid.jpeg`) rather than icon rows.
- If a design truly needs icons beyond these, use thin 1.5px-stroke geometric line icons (Lucide is the closest CDN match) in `--muted`/`--gold` — **flag this as a substitution**; nothing in the sources uses them.

## Index

- `styles.css` — global entry; imports everything under `tokens/` + `css/starzl-site.css`.
- `tokens/` — `colors.css` (website + deck palettes, semantic aliases), `sent.css` (SENT dust/ember themes), `typography.css`, `spacing.css`, `fonts.css` (Google Fonts imports — **no binaries in repo; flagged below**).
- `css/starzl-site.css` — port of the website class system (`.button`, `.eyebrow`, `.section-header`, `.metric`, `.plain-list`, `.field`, …); opt in with `<body class="starzl-site">`.
- `assets/brand/` — logo SVG suite + deck lockup PNG. `assets/images/` — 8 curated brand photographs + 2 deck diagrams.
- `guidelines/` — foundation specimen cards (the Design System tab).
- `components/site/` — website primitives (namespace `window.StarzlEnterprisesDesignSystem_64b552`):
  - `core/`: **Button**, **Kicker**, **Pill**, **CardLink**, **PlainList**, **BrandLockup**
  - `data/`: **Metric**, **MetricGrid**, **ProofItem**
  - `chrome/`: **SiteNav**, **SiteFooter**, **SectionHeader**, **Field**
  - `cards/`: **OfferingCard**
- `components/sent/` — SENT dashboard primitives (classes in `css/sent-components.css`):
  - `primitives/`: **SentButton**, **SentChip**, **SentCheckbox**, **SentSearch**, **SentSelect** (+ **SentRoleSelect**), **RoleTag** (+ **KindPill**), **MethodTag**
  - `identity/`: **SentAvatar** (+ **SentAvatarStack**), **SentBrandMark**, **SentSigil**, **SentBackdrop**
  - `data/`: **SentStatTile**, **SentStatusPill**, **SentPriority**, **SentProgress**, **SentRailPanel** (+ **SentKV**), **SentSyncIndicator**
  - `rows/`: **SentOpRow**, **SentTaskRow**, **SentActivityItem**, **SentComment** (+ **SentComposer**), **CouncilRow**, **KeyRow**, **ApiCallRow**
- `ui_kits/website/` — interactive marketing-site recreation (Home / Capability / Products / Contact).
- `ui_kits/sent_ops/` — the SENT Ops Dashboard prototype, copied verbatim from the design handoff (ground truth; 4 views, seeded data, dust/ember themes).
- `slides/` — Quicksilver deck sample slides (title, section divider, content+takeaway, stats, ledger table, closing).
- `templates/` — starting-point templates for consuming projects (Quicksilver briefing deck).
- `research/` — extracted deck text + media.
- `SKILL.md` — agent skill entry point.

## Caveats & intentional additions

- **Fonts are Google-hosted, not vendored.** No `@font-face` binaries exist in any source; `tokens/fonts.css` uses Google Fonts `@import`. Deck faces are system Arial/Courier New. If Starzl has licensed font files, add them under `assets/fonts/` and replace the imports.
- **`.card-surface` class** is an intentional addition unifying the site's 12 identical card classes (`.proof-item`, `.decision-card`, `.fit-card`, …) — same values, one name.
- The website defines **no Toast/Modal/Tabs/Tooltip**; none were invented. SENT's modal/tab patterns live only in its kit CSS.
