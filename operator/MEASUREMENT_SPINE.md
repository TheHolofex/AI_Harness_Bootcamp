# Measurement spine — Move 4

**Ultra-light week scoreboard.** Living Markdown in the Codex project.  
Updated **once per block, after adversarial review** — before the Transfer pulse.

Not a second curriculum. Not a metrics religion.  
Four headlines that answer: *Did the operator circuit actually run, and what did it cost in time and quality?*

```text
Ritual health · Mission accomplishment · Work quality · Time to result
```

---

## Purpose

| Audience | Use |
|---|---|
| **Student** | See the week as one circuit; spot ritual skips, hollow wins, and slow/fragile work |
| **Facilitator** | Thin rollup (end of file / copy rows) — who’s stuck on ritual vs mission vs quality |
| **Transfer** | 30-day rhythm inherits the same four headlines on one real workload |

---

## How it lives

| Rule | Detail |
|---|---|
| **Where** | `operator/MEASUREMENT_SPINE.md` in the Codex project |
| **Thread** | Prefer short update in `Operator — Direction & Log` after adversarial (or a dedicated `Operator — Measurement` thread if the log thread is crowded) |
| **When** | **End of every block only**, after `ADVERSARIAL:` line exists |
| **How** | Interactive with AI: you report facts; AI challenges inflated quality scores and missing times |
| **Weight** | 3–5 fields. If it takes more than ~3–5 minutes, you’re over-measuring |

### Pulse position

```text
Brief → Mission → Log + PASS_BARS draft
  → Adversarial (new thread)
  → Measurement spine row (this file)
  → Transfer pulse
```

---

## The four headlines (every block)

### 1. Ritual health — did the operator circuit run?

Score **0–3** (one point each, no partials):

| Point | Earned only if |
|---|---|
| +1 Brief | LIVE Direction Brief (all five fields) before mission |
| +1 Log | Operator Log complete including provisional verdict + evidence pointers |
| +1 Adversarial | New adversarial thread run; `ADVERSARIAL: stood/wounded/failed` line in log |

**Ritual = 3** is the floor for claiming the block was operated, not merely attended.

### 2. Mission accomplishment — did the block outcome exist?

| Mark | Meaning |
|---|---|
| **HIT** | Stated outcome exists and matches the LIVE brief’s “done looks like” |
| **PARTIAL** | Something shipped; brief outcome not fully met (name the gap) |
| **MISS** | Outcome not there; honest fail |

Mission is about **the artifact/state**, not effort and not MVP stretch goals.

### 3. Work quality — would a skeptical peer trust this?

| Mark | Meaning |
|---|---|
| **STRONG** | Adversarial **stood**; MVP claims mostly SURVIVES; evidence is peer-auditable |
| **ADEQUATE** | Usable under **wounded** or ACCEPT WITH FIXES; gaps named |
| **WEAK** | Adversarial **failed** or vibe-heavy; MVP not yet / dead claims dominate |
| **N/A** | Only if mission MISS and no artifact to judge (still say why) |

Quality is **not** “I worked hard.” It tracks evidence survival under fire.

### 4. Time to result — how long from live brief to adversarial line?

Record **minutes** (integer):

`time_to_result = clock from Direction Brief status LIVE → ADVERSARIAL line written`

Optional note (≤5 words): e.g. `setup drag`, `rabbit hole`, `clean run`.

No stopwatch theater: honest estimate is fine; fiction is not.

---

## Block rows (fill every block)

| Block | Ritual 0–3 | Mission HIT/PARTIAL/MISS | Quality STRONG/ADEQUATE/WEAK | Time (min) | One-line note |
|---|---|---|---|---|---|
| B0 | | | | | |
| P1 | | | | | |
| P2 | | | | | |
| P3 | | | | | |
| P4 | | | | | |
| P5 | | | | | |
| P6 | | | | | |
| P7 | | | | | |
| P8 | | | | | |

### Running totals (update when a row is added)

| Total | Value |
|---|---|
| Blocks logged | |
| Ritual perfect (3/3) count | |
| Mission HIT count | |
| Quality STRONG count | |
| Median time_to_result (min) | |
| Adversarial stood / wounded / failed counts | |

---

## Deep marks (only on the block that creates them — still one line)

Ultra-light continuity for the big instruments. Fill **only when that block runs**; don’t invent parallel scorecards.

| Block | Deep mark (one line) |
|---|---|
| **P2** | Dyno: baseline → after on `instruments/p2_dyno` D01–D05 (`n/5`) |
| **P3** | Comparator on `BRIEF-v1`: disagreements · kills · verdict |
| **P5** | Containment: 3/3 catches · absence-of-effect proof pointer |
| **P6** | Contract: stop/restart · exception drill pass/fail |
| **P8** | Hold/degrade D01–D05 open vs home (`n/5`) · policy refuse · transfer SEALED |

These feed quality and transfer; they do **not** replace the four headlines.

---

## End-of-block prompt (paste after adversarial)

```text
Measurement spine update. Read operator/MEASUREMENT_SPINE.md.

Block: [B0/P1/…].
Adversarial line: [paste ADVERSARIAL: …].
Brief LIVE at: [time or “approx”].
Adversarial done at: [time or “approx”].
Mission outcome path(s): [paths].
Draft MVP: [met / not yet summary].

Fill this block’s row:
1. Ritual 0–3 with proof of each point
2. Mission HIT/PARTIAL/MISS against the LIVE brief
3. Quality STRONG/ADEQUATE/WEAK from adversarial + evidence (challenge inflation)
4. Time to result in minutes
5. One-line note
6. Deep mark if this is P2/P3/P5/P6/P8

Update running totals.
Refuse cheerful quality scores without evidence.
Do not start transfer until this row is written.
```

---

## Facilitator rollup (thin)

Copy or glance at student **Running totals** + any row with Ritual &lt; 3, Mission MISS, or Quality WEAK.

| Student | Blocks | Ritual 3/3 | HIT | STRONG | Med min | Flags |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |

**Flags (use codes):** `R` ritual leak · `M` mission miss · `Q` quality weak · `T` time outlier · `A` adversarial skip  

Facilitator does not need a second database. Rescue = restore ritual and evidence, not add metrics.

---

## How to read the spine (student)

| Pattern | Likely issue |
|---|---|
| High HIT, low quality | Shipping without mastery — adversarial is doing its job |
| Strong quality, slow time | Craft OK; scope or fluency bottleneck |
| Ritual &lt; 3 with any HIT | Attendance theater — block doesn’t count as operated |
| Fast time, weak quality | Speed without judgment |
| Quality rises P2→P8 while time stabilizes | Circuit is compounding (what we want) |

---

## Transfer bridge

At P7/P8 transfer draft, copy the four headlines into the 30-day rhythm for **one real workload**:

- Ritual: brief + log + (lightweight) challenge  
- Mission: outcome hit rate on that workload  
- Quality: evidence standard under challenge  
- Time: time-to-accept or time-to-result  

Same spine, smaller world.

---

## Identity lock

If the spine becomes a wall of KPIs, cut it back to four headlines.  
If rows are filled before adversarial, delete them — measurement follows attack.  
If facilitators grade people on speed alone, the school has betrayed mastery.
