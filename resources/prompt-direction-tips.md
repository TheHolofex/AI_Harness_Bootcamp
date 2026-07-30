# Prompt & direction tips for AI harnesses

> You do not need to be a programmer to direct a harness well. You need clear intent, the right context in the window, and a way to know when the answer is good enough. This handout is the standing reference outside the block workflow.

Course tie-in: use these habits with your **Direction Brief**, **Operator Log**, **Pass Bars**, and twin-engine stack (**Codex app** home + **OpenCode** required; Claude Code optional).

---

## 0. Two skills, not one slogan

| Skill | What you optimize | When it matters |
|-------|-------------------|-----------------|
| **Prompt / direction** | The instructions you author this turn | Every brief, every repair, every ask |
| **Context engineering** | Everything the model can see: files, tools, memory, history, tool results | Multi-step harness sessions |

Modern agentic work fails more often from **bad context** than from a slightly clumsy sentence. A mediocre prompt in a clean, high-signal window usually beats a clever prompt in a polluted one.

**Operator rule:** Before you polish wording, ask: *What is in the window, and does it earn its tokens?*

---

## 1. Be specific

The gap between useful and useless is almost always specificity.

| Weak | Stronger |
|------|----------|
| "Make a website" | "Create a small local web app with a home page and an /about page. Home shows a one-line welcome. About lists these people: [paste]. Use plain HTML/CSS first; no framework unless I ask." |
| "Fix the bug" | "The /api/users endpoint returns 500 when the DB has zero rows. Full traceback below. Fix the null path and add a regression check." |
| "Make it better" | "Search takes ~3s. Profile the hot path, name the top two costs, and propose changes that target <500ms on this machine." |
| "Add a database" | "Add SQLite to the existing app. Table `tasks`: id, title, status, created_at. Routes to create and list only." |

**The rule:** If a sharp coworker would need clarifying questions, the brief is still too thin.

Name **format**, **audience**, **constraints**, and **done**. Prefer positive instructions ("Return only the complete file") over long lists of "don'ts."

---

## 2. Give context — then stop dumping

Harnesses work best when they know **what** you are building and **why**. Front-load that. Do **not** paste the whole repo "just in case."

**Without context:**  
> "Add a route that handles authentication."

**With context:**  
> "Inventory web app for a small warehouse. Python/Flask + SQLite. Already has list/add item routes. Add login with session cookies against a `users` table. Unauthenticated users redirect to `/login`. Keep offline-friendly; no cloud IdP."

**Usually include:**
- Language / stack / OS (this course: vanilla Windows 11 unless noted)
- What already exists (paths, commands that work)
- End goal and non-goals
- Hard constraints (offline, no new dependency, must match existing style)
- How you will judge success (pass bar)

**Context engineering habits (2025–2026 practice):**
- Prefer **just-in-time** reads (`@file`, open paths, "inspect `src/…`") over dumping twelve files up front.
- Keep a short standing memory (`AGENTS.md`, project notes, or your Direction Brief) with invariants — not a junk drawer.
- Separate **instructions** from **untrusted data** (logs, web pages, pasted emails) with clear markers so data is not treated as orders.
- Budget the window: history, tool spam, and giant traces rot attention ("context rot"). Compact or restart when signal drops.

---

## 3. Paste errors — still the #1 repair skill

When something breaks, paste the **full** error into the harness.

```
The app crashed after I ran the health check. Full error:

Traceback (most recent call last):
  File "app.py", line 42, in get_user
    user = db.query(User).filter_by(id=user_id).first()
AttributeError: 'NoneType' object has no attribute 'query'

I was on the OpenCode session against the local repo. What does this mean and how do we fix it without changing unrelated files?
```

**Why it works:** Tracebacks carry file, line, and failure mode. Harnesses are strong at that shape. You do not need to understand the error first — you need to deliver it complete.

**Tips:** Full traceback · nearby log lines · exact command · what changed last · which engine (Codex app vs OpenCode).

---

## 4. Iterate — small batches, testable steps

Do not ask for the whole system in one shot.

**Instead of:** one giant "build everything" prompt.

**Do:**
1. Scaffold + data shape  
2. One vertical slice you can run  
3. Next feature  
4. Auth / export / polish only after the slice is green  

**Why:** Each step is checkable. Failures localize. Twin-engine comparison stays fair when the brief is frozen and the batch is small.

This is the same physics as the [Velocity paradox](./velocity-paradox.md): friction up front, momentum later.

---

## 5. When the output is wrong — five checks

| Check | Ask | Fix |
|-------|-----|-----|
| **Context** | Does it know the mission and stack? | Restate project + paths + constraints |
| **Role / altitude** | Is guidance too vague or too brittle? | Goal + constraints, not a 40-step flowchart |
| **Specificity** | Exact behavior named? | "Monthly summary route" beats "improve it" |
| **Format** | Shape of output named? | "Complete files" · "table" · "diff only" |
| **Evaluation** | How do we know pass? | Point at Pass Bars / tests / manual check |

**Weak:** "Make a dashboard for my inventory app."

**Stronger:** "Flask + SQLite inventory app with CRUD routes. Add `/dashboard` showing total SKUs, items below reorder 10, and five newest items. Return route + template as separate files. Comment for a team new to Flask. Do not refactor unrelated modules."

---

## 6. When to restart (and when to go adversarial)

**Restart or compact when:**
- Same wrong fix loops  
- Edits thrash (apply → revert → reapply)  
- Phantom files / lost project shape  
- Window is long, slow, and unfocused  
- Mission changed; old context is dead weight  

**Before you leave the chat:** save working diffs, last error, and a short "works / broken / next" note for the new session.

**Fresh start pattern:**
> "New session. Working tree is at [path]. Done: [bullets]. Broken: [error or behavior]. Non-goals: [list]. First task: [one slice]. Review the tree, then propose a plan before editing."

**Adversarial (course Move):** for judgment calls, open a **new chat** with a frozen attack prompt against your artifact. Do not argue with the same chat that built it — that chat is contaminated by commitment.

---

## 7. Common mistakes

| Mistake | Why it fails | Do instead |
|---------|--------------|------------|
| Vague ("make it work") | Model fills gaps with defaults | Name behavior + pass bar |
| Too much at once | Partial, buggy blobs | 2–3 step slices |
| Not reading the reply | Missed warnings and file paths | Read full response before run |
| Ignoring errors | Compound failure | One error → green → next |
| "It doesn't work" with no artifact | No signal | Paste error, screenshot path, or command output |
| Assuming infinite memory | Early facts drop out | Restate invariants; use memory files |
| Dumping the whole corpus | Context rot / distraction | Point, then let the harness retrieve |
| Skipping verification | Fast draft, slow cleanup | Tests, health check, twin-engine spot check |

---

## 8. Harness tips for this bootcamp stack

### Codex app (home engine)
- Keep **build** work in the mission chat; keep **brief / log / pass bars** in the Operator chats (see Operator pack). Name and pin chats so you can find them a day later.
- **`/plan` before you edit** on anything non-trivial. It investigates and proposes an approach without touching files, which is the machine-readable version of freezing your brief.
- **Steer, don't restart.** A follow-up message joins the run in progress; queue it instead when it should wait for the next one. Killing a run to retype the prompt loses the context you already paid for.
- **`/review` your own work** before you accept it — against a base branch or over uncommitted changes. It reports findings without touching your tree, and inline comments on specific lines are treated as direction.
- **Set the permission mode deliberately.** *Ask for approval* keeps the workspace boundary and pauses at the edge. *Approve for me* keeps the same boundary but sends the escalation to an automatic reviewer instead of to you. Neither widens the sandbox — they change **who reviews**, which is a different decision from what is allowed.
- **Use a worktree when you want two things running at once.** Parallel chats in one folder will fight over the same files; a worktree gives each an isolated checkout, and *Hand off* moves a session between the worktree and your working copy without the Git argument.
- **Put standing conventions in `AGENTS.md`** at the project root. It loads every session, so it is the difference between a rule you re-type and a rule the machine already has. Add a line only after you have watched the same correction twice.
- **Ask for subagents explicitly** when work is read-heavy and separable — "spawn two agents to survey X and Y." They return summaries rather than raw output, which keeps the main chat readable. Be wary of pointing several at the same files to write.
- **Know what the app loaded before you call a run evidence.** `AGENTS.md` from the project root, `~/.codex/AGENTS.md`, discovered skills, and memories if you enabled them all arrive without appearing in your prompt. That is the whole point on a build day and a problem on a comparison day: run a frozen brief inside your P2 project and Codex is carrying your craft while the other engine runs bare. Run it clean or declare what was live.

### OpenCode (second harness)
- **Treat it as a harness, not a second chat box.** Standing conventions go in `AGENTS.md` at the project root — same move as the Codex section above, and `/init` will draft one from the repo. Agents, permissions, and custom tools live in `.opencode/` beside it. Directing a second harness is the point of P3; running a second brand is not.
- **Keep it independent whenever the run is evidence.** OpenCode reads `~/.claude/CLAUDE.md` and `.claude/skills` when it finds them, so two engines can quietly share one memory file and agree for the wrong reason. `OPENCODE_DISABLE_CLAUDE_CODE=1` is set in pre-work; add `--pure` to skip installed plugins on any run you intend to compare or log.
- **`opencode run "…"`** for one-shot terminal asks; an interactive session for multi-step repair. Pin the model per run with `-m` — model resolution otherwise falls back to whichever you used last, which is state you can't see in the transcript.
- **Permission rules are last-match-wins.** A later `allow` overrides an earlier `deny`, which is the opposite of the instinct most people bring from other tools. Write broad rules first and exceptions after, and read your own config bottom-up when you're asking why something was permitted.
- **Wrong model choice is a context problem wearing a prompt problem's clothes.** `opencode models <provider> --refresh` before you rewrite the brief.
- **`/undo` reverts the file changes, not just the message.** It needs a Git repo to do it. Know that before you reach for it mid-repair.
- Custom providers and local endpoints are configured under `provider` in `opencode.json` — that seam is what you re-point during hold-and-degrade (P8).

### Optional: Claude Code
- Strong when you want a second adjudicator; not required for the core path.
- Same rules: small batch, full errors, explicit pass bar.

### Twin-engine habit
Same frozen brief → both engines → compare on **evidence**, not vibes. Log the delta in the Operator Log.

Before the delta means anything, check what each side was carrying: instruction files, skills, memories, plugins, and which model actually answered. Both engines load context you didn't type, and neither announces it. One engine plus your notes is not two engines — run clean, or declare what was live.

---

## 9. Direction starters (copy / adapt)

```
I have a [stack] project at [path] that [mission in one sentence].
Constraints: [OS / offline / libs / style].
Already true: [what works].
Task: [one slice].
Done when: [pass bar].
Please [plan only | edit | review only]. Do not expand scope.
```

```
Error while [command / action]:

[full traceback or log]

Engine: [Codex app | OpenCode]. Last change: [one line].
Fix the failure with minimal diff; add a check so it cannot silently return.
```

```
Review [path] against these pass bars: [bullets].
List gaps only. Do not rewrite yet.
```

```
New adversarial chat. Artifact under test: [path or paste].
Attack prompt: [frozen].
Return: findings ranked by severity, with a one-line fix hypothesis each. No pep talk.
```

```
Summarize this session for handoff: works / broken / files touched / next slice.
Max 12 lines.
```

---

## 10. Quick link to course instruments

- Direction Brief · Operator Log · Pass Bars · Adversarial review · Measurement spine · Transfer 30-60-90 → Operator pack  
- P2 Dyno · P3 Frozen brief · P8 Hold/degrade → Instruments  
- Why slow foundation beats rushed codegen → [The velocity paradox](./velocity-paradox.md)

---

*The best direction is one a sharp colleague could act on without a follow-up. If you would need to clarify for a human, clarify for the harness — and put only high-signal tokens in the window.*
