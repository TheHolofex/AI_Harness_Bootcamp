# The velocity paradox: slow start, fast finish

In AI-assisted work, speed is **non-linear**. The efficient path to a finished artifact usually includes an early stretch of deliberate friction. That friction is not delay. It is how you shrink the hallucination surface so later execution can run hard.

This handout is a standing resource for the AI Harness Bootcamp. It pairs with Direction Briefs, Pass Bars, and the measurement spine.

---

## 1. The phase shift

### Phase A — Reasoning over possibilities (slow)

- **Activity:** Clear ambiguity. Name success. Define interfaces and data shapes. Stand up verification (tests, lints, health checks, pass bars). Write the brief.
- **Feels like:** Pedantic, recursive, "are we there yet?"
- **Goal:** **Contextual gravity.** Rigid enough constraints that the harness stops guessing intent and starts filling a known shape.

### Phase B — Reasoning over artifacts (fast)

- **Activity:** Implement features, wire UI, expand boilerplate, twin-engine compare on a frozen brief.
- **Feels like:** Momentum. You are driving.
- **Goal:** High-fidelity delivery. The model is anchored by real files, real failures, and a real definition of done.

Skipping A does not get you to B early. It gets you **architectural drift**: plausible code aimed at unstated goals, plus a long cleanup tax.

---

## 2. Visualizing velocity

```
       ^
       |                                       /--- [DONE]
       |                                      /
       |                                     /  (PHASE B)
    V  |                                    /   MOMENTUM
    E  |                                   /    Reasoning over
    L  |                             _____/     Artifacts
    O  |                       _____/
    C  |                 _____/
    I  |           _____/
    T  |     _____/   (PHASE A)
    Y  |____/         FOUNDATION
       |              Reasoning over
       |              Possibilities
       +--------------------------------------------------->
                          PROGRESS / TIME
```

Early slope is shallow on purpose. Later slope is steep because uncertainty was paid down.

---

## 3. Why this is sharper in the agent era

Three facts from current practice (directionally consistent across DORA-style delivery research, controlled studies on AI coding, and production agent write-ups):

1. **Drafting got cheaper.** Boilerplate, first cuts, and navigation are fast.
2. **Verification did not disappear.** Review, integration, and "is this the right thing?" still dominate real calendars. If generation outruns checks, queues move downstream (review, rework, incidents).
3. **Context beats clever wording.** Long windows still suffer **context rot**. More tokens are not free intelligence. Small, high-signal context plus a crisp pass bar outperforms a dump of the monorepo.

So the paradox has two faces:

| Face | What you notice |
|------|-----------------|
| **Personal** | Slowing down to brief and test makes the afternoon feel faster. |
| **System** | Speeding only the inner coding loop can slow the org if review and verification stay manual and overloaded. |

This course trains the personal face first: operator judgment, cothinking, and instruments you own.

---

## 4. Logical building blocks (Possibility → Artifact)

Lock these before you ask for volume:

1. **The Anchor — success**  
   What does "good" mean in observable terms? (Pass bars, acceptance checks, "done when…")

2. **The Harness — verification**  
   How do we know? (Commands you can re-run, health check gate, twin-engine spot check, CI if you have it.)

3. **The Interface — shape**  
   How do pieces talk? (Data models, file boundaries, API contracts, non-goals.)

4. **The Context pack — what the model may see**  
   Standing invariants, relevant paths, frozen brief. Not the entire history of the chat.

If any block is missing, you are still in Phase A — even if the model is already emitting files.

---

## 5. Course mapping (use the instruments)

| Paradox move | Bootcamp instrument |
|--------------|---------------------|
| Name success before code | Pass Bars · Direction Brief |
| Keep judgment out of build chat | Operator chats (brief/log vs mission) |
| Attack your own certainty | Adversarial review in a **new** chat |
| Prove learning transferred | Transfer 30-60-90 · Transfer gates |
| Evidence over vibes | Measurement spine · P2 Dyno |
| Fair engine compare | P3 Frozen brief (same brief, two engines) |
| Hold quality when the stack degrades | P8 Hold / degrade |

**Daily pulse:** AM brief (Phase A minutes) → build (Phase B) → PM log + bars + measure. Do not skip the bookends because the middle feels productive.

---

## 6. Anti-patterns (false speed)

| Anti-pattern | What actually happens |
|--------------|----------------------|
| Skip the brief; "just build" | Model invents requirements; you debate ghosts later |
| One mega-prompt for the system | Partial blob; cannot localize failure |
| Giant diffs | Unreviewable; twin-engine compare becomes theater |
| No pass bar | You cannot tell progress from motion |
| Same chat forever | Context poison + commitment bias |
| Optimize only lines/minute | Verification debt compounds; delivery flatlines |
| Treat green demo as done | Integration and ops were never in the window |

---

## 7. Operator checklist (before you "drive")

- [ ] Mission in one sentence; non-goals listed  
- [ ] Done-when / pass bars written where you will actually look  
- [ ] Interfaces or file touch-list named  
- [ ] Verification command or manual check exists  
- [ ] Context pack is lean (paths + invariants, not a dump)  
- [ ] Batch size is one vertical slice  
- [ ] Engine choice noted (Codex app / OpenCode / both)  
- [ ] Plan for adversarial or twin-engine check if the stake is high  

Only then spend tokens on volume.

---

## 8. The engineering mandate

**Do not rush the friction.**

Attempts to skip straight to driving usually produce architectural drift and a cleanup bill larger than the "slow" hour you avoided.

> Slow is smooth, and smooth is fast.

In harness terms: **brief hard, batch small, verify early, then let the engines run.**

---

## 9. Further reading (orientation, not required)

- Course: Operator pack, Measurement spine, P2/P3/P8 instruments  
- Prompt & direction tips (companion handout in this folder)  
- Industry orientation: delivery research on AI adoption vs instability; controlled studies on AI coding time; practitioner notes on context engineering and "generation outrunning verification"

---

*Velocity you cannot verify is just acceleration toward rework. Pay for clarity in Phase A; collect speed in Phase B.*
