# Adversarial review — in-course verdict challenge

**Mandate:** deep operator mastery requires verdicts that survive attack — not only self-check.

The challenger you can always get is a **fresh AI chat with a frozen adversarial prompt**, run **every block** after you have results. It is available at eleven at night, it has no stake in your feelings, and it will read the whole pack.

A human who can challenge your verdicts is a different and better thing, and it is what you are building toward on the job (see `TRANSFER_30_60_90.md`). One does not replace the other. At P8 the ninety-second defense goes to a live listener precisely because a person can refuse to be convinced in a way a prompt cannot.

```text
You own the verdict.
This chat’s job is to try to take it away — with evidence rules, not vibes.
```

---

## Where it sits in the half-day pulse

```text
1. Direction Brief     →  chat: Operator — Direction & Log
2. Mission             →  build chat(s)
3. Operator Log
   + PASS_BARS draft   →  Direction & Log
4. Adversarial review  →  NEW chat every time (below)   ← you are here
5. Fix or stand firm   →  update Log / bars if the attack lands
6. Measurement spine   →  MEASUREMENT_SPINE.md row (three entries)
7. Transfer            →  chat at B1, P7, P8; a dated seed line at the others
```

**Why a new chat each time:** clean context. No build-chat cheerleading, no log-chat collusion. Paste artifacts in; the reviewer never “helped you succeed” five minutes ago.

---

## Rules

| Do | Don’t |
|---|---|
| New chat every block (title below) | Reuse the build chat for “review” |
| Paste **outputs + paths + your provisional verdict** | Ask “does this look good?” |
| Require the model to argue **not yet** hard | Accept praise or summary-only feedback |
| Change the log if the attack is valid | Performatively “take notes” and change nothing |
| Keep human peer as **job** outer-loop name | Pretend AI review replaces institutional challenge forever |

---

## Which engine reviews you

One rule, and it has no exceptions:

> **Where a second engine is already open, the review runs in the second engine. Everywhere else it runs in a new chat in the same engine.**

| Block | Reviewer | Why it is free there |
|---|---|---|
| **P3** | **OpenCode**, second pass on the same pack | OpenCode is already running from Stage 03 with the cargo flags set |
| **P5** | **OpenCode**, second pass on the same pack | OpenCode is already running from the probe folder |
| **P8** | **The re-pointed hosted open model**, second pass on the same pack | You wired that endpoint this morning and trusted it enough to run D01–D05 |
| B1, P1, P2, P4, P6, P7 | New chat, same engine | No second engine is open, and opening one costs more than the pass is worth |

At P3, P5 and P8 the second engine is a **second pass on the pack you already assembled** — same frozen prompt, same excerpts, no softening, run after the first review is done. It is not a replacement for the first pass and it is not a lighter one. Record **both** final `ADVERSARIAL:` lines in the log, side by side and labelled by engine or endpoint.

**Where the two engines disagree about a bar, the disagreement is the finding.** Name it in the log. One reviewer accepting an absence-of-effect proof that the other rejects tells you which of the two had the blind spot, and it is not always the one you expect. If they agree, that is information too — it does not make the claim true, it makes it un-attacked by two readers of the same pack.

A third pass in a third engine is available if you want it and proves nothing extra you cannot already see.

---

## Chat title pattern

`Adversarial — [block] — [date]`  

Example: `Adversarial — P3 Twin-engine — 2026-03-18`

One block · one chat · then archive. Do not keep a single season-long adversarial chat.

---

## What you bring (paste pack)

Minimum paste into the new chat:

1. Block name + one-line mission outcome  
2. Link/paths to key artifacts (brief path, outputs, comparator, vault notes, contract, etc.)  
3. Your **provisional** Log verdict (`ACCEPT` / `REJECT` / `ACCEPT WITH FIXES`)  
4. Your **draft** MVP self-check — which bars you marked met, **and how many**  
5. Anything you already know is weak  

Item 4 carries a number for a reason. The count of bars you marked met is the denominator of your overclaim, and it has to be fixed before the reviewer speaks. Write it down, paste it in, and do not revise it afterwards — a denominator chosen after the verdict is not a denominator.

If the model cannot see files, paste the critical excerpts (comparator rows, test output, citation sample, stop proof). Thin excerpts produce a polite reviewer, and a polite reviewer is not a pass.

---

## Frozen adversarial prompt (paste every time)

```text
You are an adversarial operator reviewer for an operator’s school.
Your job is NOT to help me feel successful. Your job is to stress-test my verdict and MVP claims.

Context: deep operator mastery of AI direction and cothinking.
Evidence beats vibe. Model self-praise is not evidence. Agreement is not truth.
Containment is absence of effect. Autonomy without stop proof is theater.

I will paste: block, artifacts/paths/excerpts, provisional verdict, draft MVP checklist.

Protocol — follow in order:
1. Restate my claimed outcome and verdict in one cold sentence (no praise).
2. Attack pass: give the strongest case that this is NOT YET mastery for this block.
   - Demand missing evidence (paths, tests, trails opened, comparator kills, stop proof, etc.).
   - Name completion theater if you see it.
   - If you cannot find a serious attack, say what you checked and what would still worry a skeptical peer.
3. Evidence audit: for each MVP claim I marked met, mark:
   SURVIVES / WOUNDED / DEAD — with reason.
4. Verdict challenge: argue whether my ACCEPT/REJECT/ACCEPT WITH FIXES is earned.
   If ACCEPT, try to force ACCEPT WITH FIXES or REJECT.
   If REJECT, check I am not rejecting to avoid measurement.
5. Force one of:
   a) Concrete fix list (smallest changes to reach real MVP), or
   b) “Stands under fire” — only if evidence is actually strong.
6. End with a single line I must copy into my Operator Log:
   ADVERSARIAL: [stood / wounded / failed] — [one sentence].

Rules for you:
- No encouragement fluff. No “great job.” No emoji.
- Do not rewrite my mission for me unless citing a fix.
- Do not accept screenshots of chat enthusiasm as evidence.
- Prefer false NOT YET over false pass.
- Short, sharp, specific.
```

---

## After the attack (required)

Back in `Operator — Direction & Log` (or edit files directly):

| If review says… | You must… |
|---|---|
| **Stood under fire** | Log the ADVERSARIAL line; write the measurement row |
| **Wounded** | `ACCEPT WITH FIXES` or fix now; note what changed under fire |
| **Failed / dead MVP items** | Status **not yet** on those bars; fix or schedule fix before leaving block |

### Write down what the attack took away

Before you close the chat, copy the per-claim rulings out of it. Name **every** claim the review marked `WOUNDED` or `DEAD` and what you did about each one — fixed it, re-evidenced it, or accepted the wound and unticked the bar.

An empty list is a legitimate answer and is worth having on the record.

That list is the only place the rulings survive, and the measurement row is counted from it: the bars that came back wounded or dead, over the number you marked met, is your **overclaim** for the block. Counting it from your own summary of the chat instead of from the rulings turns it back into a number you awarded yourself.

Measurement spine row is written only after the adversarial line exists.  
At B1, P7 and P8, the Transfer chat starts only after the measurement row exists.
The outer loop should not inherit unchallenged fantasy.

---

## Who else can challenge a verdict

| Setting | Challenger |
|---|---|
| **Every block** | Adversarial AI chat, new every time (this file) |
| **P3, P5, P8** | A second engine on the same pack — required, not a stretch. See *Which engine reviews you* above |
| **Pair moments (optional)** | Human peer uses the same frozen prompt on your paste pack |
| **After course (transfer seed)** | Named human who can challenge verdicts on the job |

An AI challenger trains the *habit*: you learn to assemble a pack, take the hit, and change the log.  
A human challenger trains *institutional* honesty: someone whose good opinion costs you something has read your evidence and disagreed. Build the habit first; the habit is what makes the human conversation short enough to actually happen.

---

## Facilitator notes

- **Watch the engine-disagreement rate at P3, P5 and P8.** Two engines reading the same pack should differ on something. Near-zero disagreement across a cohort almost never means the work was clean — it means the packs are too thin to tell two reviewers apart. Go and read a pack before you read the verdicts.
- A polite reviewer is the same signal one engine at a time: the student under-pasted or reused the build chat.
- Time box: **5–8 minutes** standard; **10–12** at P3, P5 and P8, where the pack is reviewed twice.
- Rescue: narrower artifact paste, not a softer prompt.
- Never replace PASS_BARS with “the AI said it’s fine.” Bars still need evidence pointers.

## Identity lock

If adversarial review becomes “ask the same chat if we’re good,” the school has collapsed into vibe with extra steps.  
**New chat. Frozen prompt. Evidence. Log the scar.**
