# Direction Brief

Standing operator file in the Codex project.  
Maintained only in the **`Operator — Direction & Log`** thread — not in build threads.

**How it gets written:** you and the AI produce this **interactively**. The AI interviews, drafts, and challenges vagueness. **You** accept or rewrite every field. The machine does not run the mission until you say the brief is live.

Five fields. Target: under five minutes of dialogue.

---

## Block / mission

<!-- set during the interview -->


## 1. Outcome

What must exist when this is done? Artifact or state — not activity.


## 2. Done looks like

Observable checks only (open, run, compare, count). If it can’t be checked, it isn’t a criterion.


## 3. Bounds

What the machine must **not** do — paths, tools, data, actions, scope.


## 4. Evidence standard

What counts as proof for accept. Model self-assessment does **not** count.


## 5. Stop / hand-back

When the machine stops and returns control — failure modes, time box, or “ask before X.”


## Status

- [ ] Draft in progress (AI + operator)
- [ ] **LIVE** — operator accepted; mission may run
- [ ] Superseded mid-run (see log)

---

## Operator-thread starter (paste this to begin)

```text
We are writing the Direction Brief for this block together.

Read operator/DIRECTION_BRIEF.md (or this file). Interview me in short turns.
Do not dump all five fields at once unless I already gave you a clear mission.

For each field:
1. Ask one focused question.
2. Propose tight wording from my answer.
3. Challenge anything vague, uncheckable, or unbounded.
4. Wait for me to accept or correct before moving on.

When all five fields are accepted, write them into this file, set Status to LIVE,
and remind me to run the mission in a separate build thread — not here.

After the mission, we will write the Operator Log in this same thread.
```

## Transfer

Same interactive pattern at work: open a short direction thread, produce five fields, freeze the brief, then run.
