# Course site — visual system

**Sources of truth for look and feel**

| Source | What we take |
|---|---|
| [starzl.com](https://starzl.com) | Altitude, restraint, defense-industrial composure, product/mission framing |
| `Starzl_Experience_on_Demand_Quote.pdf` | Paper document system: mark, type, rules, meta grid, tables |
| `Starzl_AI_Harness_Bootcamp_Invoice.pdf` | Same system applied to bootcamp delivery docs |

The course site is **not** a slide deck skin and **not** a consumer edtech pastel theme.  
It should feel like **Starzl courseware on the web**: operator-ready, calm, exact.

---

## Dual surface (important)

Starzl materials use two related surfaces. The course site uses **both**, with clear roles.

### A. Paper surface (default for course pages)

From the quote/invoice PDFs — **primary UI for reading and exercises**.

| Token | Value | Role |
|---|---|---|
| `--paper` | `#FFFFFF` | Page ground |
| `--paper-warm` | `#FAFAF8` | Subtle section wash (optional) |
| `--ink` | `#0A0A0A` | Primary text / rules |
| `--ink-muted` | `#4A4A4A` | Secondary body |
| `--ink-faint` | `#6B6B6B` | Meta labels, captions |
| `--rule` | `#D0D0D0` | Hairline borders / table lines |
| `--rule-strong` | `#1A1A1A` | Heavy total rules |
| `--mark` | `#E31C23` (approx crimson/red) | Starzl disc / critical accent only |
| `--accent-line` | same as `--mark` | Sparse horizontal emphasis (totals, active section) |

**PDF layout laws (carry to CSS)**

- Wide clean margins; content column centered, not edge-to-edge chrome  
- Logo lockup: **filled red disc** + `STARZL` / `ENTERPRISES` stacked or tracked wordmark, high letter-spacing  
- Document type label top-right, tracked uppercase (`QUOTATION` / `INVOICE` → site: `COURSE` / `BLOCK` / `PRE-WORK`)  
- Meta grids: 3–4 equal cells, light border box, small caps labels over values  
- Section labels: tracked uppercase, small, muted (`SCOPE OF ENGAGEMENT` → `LEARNING OBJECTIVES`)  
- Display title: large, tight, near-black serif *or* high-quality grotesque — weighty, not playful  
- Hairline rules separate bands; one crimson rule for total/emphasis only  
- Tables: minimal grid, generous cell padding, numeric columns right-aligned when money/scores  
- Footer: thin rule, signature/authority left, `inquiries@starzl.com · starzl.com` right  

### B. Defense field surface (heroes, diagrams, operate-along canvases)

From Starzl defense figure system / starzl.com altitude — **sparingly**.

| Token | Value | Role |
|---|---|---|
| `--field` | `#0D0906` | Primary dark ground |
| `--field-panel` | `#17110C` | Panels |
| `--gold` | `#A58650` | Primary signal / key UI chrome |
| `--gold-bright` | `#C8A96A` | Highlights |
| `--sand` | `#C8B78A` | Body on dark |
| `--sand-dim` | `#3A2E1B` | Footnotes on dark |
| `--warn` | `#B43A2F` | Warnings only |
| `--steel` | `#2D3030` | Neutral structure |

Use field surface for: home hero, live-demo backdrop, instrument “dyno board” moments, figure embeds.  
**Do not** force long exercise prose onto pure black — readability loses to mood.

---

## Typography

| Role | Guidance |
|---|---|
| **Wordmark** | Geometric sans, uppercase or small-caps friendly, wide tracking (`STARZL ENTERPRISES`) |
| **Display / H1** | Confident editorial: large, tight leading, minimal decoration |
| **Section labels** | 11–12px-equivalent, uppercase, letter-spacing ~0.12–0.2em, muted |
| **Body** | 16–18px web, 1.55–1.7 line-height, high contrast on paper |
| **Mono** | For paths, commands, case IDs (`D01`, `BRIEF-v1`), score cells |
| **Avoid** | Rounded consumer fonts, gradient text, heavy drop shadows, “bootcamp fun” display faces |

If web fonts are chosen later, prefer a pair in the Inter / IBM Plex / Source Serif *family of seriousness* — final faces TBD to match production starzl.com exactly when assets are available.

---

## Logo lockup

From PDFs:

```text
 ●  STARZL
    ENTERPRISES
```

- Disc is solid crimson/red — never outlined-only as the primary mark  
- Wordmark black on paper, light on field  
- Clear space ≥ disc diameter on all sides  
- Small corner placement on content pages; larger on home  

---

## Component patterns (site)

### Top bar
- Paper ground, hairline bottom rule  
- Mark + wordmark left  
- Nav: Pre-work · Week · Instruments · Operator · Track  
- No hamburger theater on desktop; quiet mobile collapse  

### Block page skeleton
1. Eyebrow: `DAY 02 · P2 · ENGINEERING TRACK` (tracked)  
2. H1: project name  
3. One-paragraph mission  
4. Meta strip (time · tools · instrument link · pulse steps)  
5. Sections with uppercase labels + hairlines  
6. Primary actions as sober buttons (black fill or crimson only for “Start mission”)  
7. Footer course chrome  

### Buttons
- Primary: near-black fill, white text, no rounded pill excess (slight radius OK)  
- Secondary: hairline border, ink text  
- Danger/accent: crimson only for irreversible or “start live”  

### Cards / instrument tiles
- White card, 1px `--rule` border, no heavy shadow (at most hairline elevation)  
- Title + one line + “Open kit →”  
- Track badge: small muted chip  

### Tables (scores, comparators)
- Match invoice tables: header row muted label style, horizontal rules, not zebra carnival  

### Code / AI panes
- On paper pages: light gray panel (`#F4F4F2`) + mono  
- Optional field-surface embed for live demo diagrams  

---

## Motion & imagery

- Motion: minimal; short fades only  
- Imagery: technical figures, diagrams, UI captures — **not** stock handshake / neon brain  
- Live operate-along may show real tool UI; site chrome stays calm around it  
- Follow figure-gen restraint when embedding Starzl figures: label-dense, no cinematic staging  

---

## Voice on the surface (learner-facing)

**Visual system = Starzl.** **Written voice = guide-beside** (warm, complete, easy to follow).

The site should *look* like Starzl courseware and *read* like a skilled operator standing next to you at the laptop.

| Principle | On the page |
|---|---|
| Purpose first | Every block/pre-work page opens with what this does for you and roughly how long it takes |
| Map before territory | Steps/shape of the whole before the first deep detail |
| Warm-neutral | “you’ll,” “don’t”; welcoming; never chummy, never cold |
| Complete sentences | Flowing prose; short complete lines at decision points — not slogan fragments |
| Concepts when needed | Define harness, brief, adversarial, dyno, etc. at first use, in plain words; add a related-concept beat when it prevents confusion |
| Failure is data | Normalize errors; give the recovery path in the same breath |
| Concrete verbs | *Run, Verify, Direct, Adjudicate, Seal* — still operator school |
| No marketing register | Not “Level up your AI journey,” “take the wheel,” confetti empty states |

**Lead operate-along** can go deeper and more experiential out loud.  
**Site copy** must still make sense when re-read alone between sessions.

Full recipe: guide-beside-voice skill · identity: `MEMORY.md` Learner-facing voice.

---

## Accessibility

- Paper mode body contrast ≥ WCAG AA  
- Crimson never the only encoding of meaning (pair with text)  
- Focus rings visible on black and paper  
- Dyno/score tables usable with keyboard  

---

## Non-goals

- Rainbow gradients, glassmorphism stacks, mascot stickers  
- Slide-deck metaphor (advancing “slides” as the course)  
- Separating a secret teacher skin from the student site — **same site**  

---

## Implementation notes (when building)

1. CSS variables for paper + field tokens above  
2. Layout max-width ~720–880px for prose; wider for tables/instruments (~1100px)  
3. Print stylesheet should still feel like the PDF system (students may print briefs)  
4. Prefer static/SSG pages from repo markdown → site routes  

## Open items

- Exact crimson hex from brand files (measure from logo SVG when available; PDF approx `#E31C23`)  
- Production webfonts matching starzl.com  
- High-res mark asset (SVG) committed under `site/assets/`  
