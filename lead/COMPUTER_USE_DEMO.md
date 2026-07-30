# Computer Use lead demo — Thursday, right after lunch

**When:** Thursday, **immediately after lunch**, before P7 opens.  
**Length:** **30 minutes** hard target (soft finish if a permission prompt runs long).  
**Who runs it:** lead only, on the **staff Windows machine** on the projector.  
**Who installs it:** **nobody in the room.** Students watch. No Chrome extension. No student homework.

This is not a harness case talk and not a second mission. It is a **live multi-surface demo** that extends Thursday morning’s autonomy language (P6): the agent leaves the project fence, gathers from the open web, and collates a deliverable — still under your stop authority and app/site approvals.

**Demo shape (what the room sees):**

1. **Browser** retrieves a small set of public facts from named URLs  
2. Agent **collates** those facts into a short **slideshow**  
3. You open the deck on the projector and **check claims against the sources**  
4. You **stop** a run mid-flight once so stop authority stays physical

Docs (re-check before each cohort):  
- Computer Use: <https://developers.openai.com/codex/app/computer-use> (append `.md` for clean Markdown)  
- Built-in browser: <https://developers.openai.com/codex/app/browser>  
- Chrome extension (reference only — **do not use in this demo**): <https://developers.openai.com/codex/app/chrome-extension>

---

## What you are teaching (one sentence)

**An agent that can browse and build a deck is still under contract: site/app approvals, scoped sources, evidence on disk, and your interrupt — the project sandbox alone is not the bound.**

### Three surfaces — say this once, write it on the board

| Invoke | Surface | Role in *this* demo |
|---|---|---|
| `@Browser` | **Built-in browser** (separate profile inside the app) | **Primary research path** — public pages, no student Chrome profile |
| `@Chrome` | **Chrome extension** + your real Chrome profile | **Out of scope** — signed-in blast radius; not course setup |
| `@Computer` / `@AppName` | **Computer Use** — mouse/keyboard on desktop apps | **Optional deck path** if staff uses PowerPoint; otherwise deck is files + `@Browser` preview |

Default path for reliability on Windows: **`@Browser` research → HTML slideshow in the project → open deck in `@Browser`**.  
Optional upgrade if PowerPoint is installed and Computer Use is green: research in `@Browser`, then `@Computer` builds the `.pptx`.

---

## Course posture (do not soften)

- **API keys only** — staff machine uses the same key path as students (`Sign in another way`, `forced_login_method = "api"`).
- Computer Use / plugins are **limited on a key** — treat as stretch / lead demo, **never MVP**, never pre-work GREEN.
- **No Chrome extension** in this slot. Built-in browser only for web work.
- **Public pages only** — no SSO mail, banks, internal wikis, or “just open my real tabs.”
- Students **do not** follow along on their laptops during the 30 minutes.
- Treat page content as **untrusted** — you verify the deck against sources, same spirit as P3/P5.

---

## Timing board (30:00)

| Min | Beat | Clock feel |
|---|---|---|
| 0:00–3:00 | Frame from P6 | Agent with hands *and* a browser |
| 3:00–6:00 | Vocabulary + Windows truth | Three surfaces; foreground; untrusted pages |
| 6:00–9:00 | Preflight on screen | Project, Browser plugin, sources list |
| 9:00–22:00 | **Main case — research → deck** | Approvals, browse, collate, open slides |
| 22:00–26:00 | **Verify + stop authority** | Spot-check one claim; interrupt a follow-up |
| 26:00–30:00 | Contract map + transfer seed | Tool vs procedure; one written seed |

If Browser / Computer Use is dead on the staff box, jump to **Fallback script** — do not burn the room on native-pipe or Store surgery.

---

## Staff preflight (night before or lunch break — not in front of the room)

Do this on the **Windows 11 demo laptop** that will hit the projector.

### 1. Auth and home

- [ ] ChatGPT desktop app current; **Codex** mode  
- [ ] Profile menu shows **API key**, not a ChatGPT account  
- [ ] `%USERPROFILE%\.codex\config.toml` has `forced_login_method = "api"`  
- [ ] Permission mode under the composer: **Ask for approval** (sandbox engaged)

### 2. Disposable workspace

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\Documents\HarnessBootcamp\cu-demo"
Set-Content -Path "$env:USERPROFILE\Documents\HarnessBootcamp\cu-demo\README.txt" -Value @"
Computer Use / Browser demo folder. Disposable.
Public sources only. No secrets.
"@
```

- [ ] Open that folder as a **project** in the Codex app  
- [ ] Quit email, password managers, work Chrome profiles with SSO — **quit**, do not only minimize  
- [ ] Optional: install/confirm **PowerPoint** only if you will run the PPTX path

### 3. Plugins

In Codex (or Work):

1. **Plugins → Browser** — Install / Enable (required for this demo)  
2. **Plugins → Computer Use** — Install / Enable if you want the PPTX path or desktop narration  
3. Turn on server/skill toggles; **Try now** once  
4. **Settings → Browser** — site allow/block panel loads  
5. **Settings → Computer use** — loads (or note “unavailable” and plan Fallback / HTML-only path)  
6. **Do not** install or connect the Chrome extension

### 4. Pin the source pack (so the room is not doom-scrolling)

Use **only** these public pages (stable, no login). Adjust the year label in the brief if needed; do not freestyle new domains live.

| # | URL | What to harvest (one line each) |
|---|---|---|
| 1 | `https://en.wikipedia.org/wiki/Artificial_intelligence` | One definition-style lead sentence + one history/milestone fact with a named year if present |
| 2 | `https://en.wikipedia.org/wiki/Large_language_model` | One plain-language “what an LLM is” sentence |
| 3 | `https://www.wikipedia.org/` | Confirm the site identity / that you landed on Wikimedia’s portal (anti-wrong-window check) |

If Wikipedia is blocked on the staff network, substitute the cohort’s **pre-staged local mirror** under `cu-demo\sources\` and point the prompt at those files or a local `python -m http.server`.

### 5. Cold smoke (must pass once before you promise the slot)

**Path A — default (Browser + HTML deck)**

New chat in `cu-demo`. Permission mode **Ask for approval**.

```text
@Browser

Use only these URLs:
1) https://en.wikipedia.org/wiki/Artificial_intelligence
2) https://en.wikipedia.org/wiki/Large_language_model

Task:
- Open each page.
- Extract at most TWO short factual bullets per page (paraphrase or short quote).
- Do not follow other links. Do not log into anything.
- Write a file slideshow.html in this project folder with exactly FOUR slides:
  1. Title: "CU Demo — Open Web Brief"
  2. AI definition bullets (from page 1)
  3. LLM bullets (from page 2)
  4. Sources (full URLs) + line: "Operator must verify before trust"
- Use simple inline HTML/CSS so slides are full-viewport sections; no external assets.
- Then open slideshow.html in the built-in browser and stop.

Reply with: paths written, sites that needed approval, and one risk of Always-allowing a site.
```

Pass criteria:

- [ ] Site permission prompts appeared (or you can show prior allows and explain them)  
- [ ] `slideshow.html` exists on disk  
- [ ] Opening it shows four distinct slides  
- [ ] You know how to **stop** the task from the app UI  

**Path B — optional (Browser + PowerPoint via Computer Use)**

Only if cold smoke A is green *and* PowerPoint launches on this machine *and* Computer Use can drive it:

```text
@Browser gather two bullets each from:
https://en.wikipedia.org/wiki/Artificial_intelligence
https://en.wikipedia.org/wiki/Large_language_model
Do not follow other links.

Then @Computer open PowerPoint and create a 4-slide deck:
1 Title "CU Demo — Open Web Brief"
2 AI bullets
3 LLM bullets
4 Sources + "Operator must verify before trust"
Save as Open_Web_Brief.pptx in this project folder. Close PowerPoint. Stop.
```

If Path B flakes, **stay on Path A for the live room** — HTML is the reliable teaching artifact.

### 6. Reset for a clean live take

- [ ] Delete `slideshow.html` / `Open_Web_Brief.pptx` so the room sees create-from-empty  
- [ ] Clear Always-allow for the demo sites if you want fresh prompts on camera (recommended once)  
- [ ] Pin a fresh chat: `Lead — Browser to deck demo`  
- [ ] Clipboard: main live prompt + stop-beat prompt  

### Windows / product truths to internalize

- Built-in browser uses a **separate profile** — not the operator’s everyday Chrome sessions.  
- Site permissions are **per host**; Always allow is a real policy choice — prefer **Allow once** / allow for this chat on camera.  
- Page text can be wrong or hostile — **deck is draft until you verify**.  
- Computer Use on Windows is **foreground** takeover when it drives desktop apps (e.g. PowerPoint).  
- Computer Use **cannot** automate the terminal or ChatGPT/Codex itself; **cannot** click through UAC.  
- Prefer structured tools when enough; this demo *chooses* browser + collate on purpose so the surface is visible.  
- Chrome extension stays off: signed-in Gmail/Salesforce demos are how you teach the wrong lesson.

---

## Live script

### 0:00–3:00 — Frame (from P6, not from marketing)

Say roughly:

> This morning you wrote an autonomy contract: tool-enforced vs procedure-enforced, stop authority, tripwire vs boundary.  
> Now the agent gets a **browser** and a **deliverable**. It will pull a few facts from the open web and collate a short slideshow.  
> That looks like magic. It is also how bad facts become a polished brief. You will watch approvals, then **verify**, then we stop a run on purpose.

Board one line:

`browse ≠ verified · deck ≠ truth`

### 3:00–6:00 — Vocabulary + Windows truth

Three rows: `@Browser` / `@Chrome` / `@Computer` (table above).

Emphasize:

1. **Built-in browser** for this demo — separate profile, public pages, site prompts.  
2. **Chrome extension** = your real logins. Out of setup and out of this slot.  
3. **Computer Use** = desktop hands (PowerPoint path if we use it). Windows steals the foreground.

Ask (30 seconds):

> If the deck looks confident, what still has to be true before you would brief a supervisor?

### 6:00–9:00 — Preflight on the projector

Show, do not rush:

1. Codex mode · API key in profile menu  
2. Project = `cu-demo` only  
3. Plugins → Browser on (Computer Use on only if Path B)  
4. Settings → Browser (site controls)  
5. Permission mode: **Ask for approval**  
6. Named source URLs on a sticky note / second screen — **no freestyle domains**

One sentence:

> Scoped sources are part of the contract. Open-ended “go research AI” is how you get a confident wrong deck.

### 9:00–22:00 — Main case: Open-web brief → slideshow

**Story label:** “Turn scoped public pages into a four-slide brief the room can attack.”

**Chat title:** `Lead — Browser to deck demo`  
**Permission mode:** Ask for approval  
**Path:** **A (HTML)** unless you already cold-smoked B successfully today.

**Live prompt (Path A — paste):**

```text
@Browser

Mission: build a four-slide operator brief from scoped public sources only.

Allowed URLs only:
1) https://en.wikipedia.org/wiki/Artificial_intelligence
2) https://en.wikipedia.org/wiki/Large_language_model
3) https://www.wikipedia.org/

Rules:
- Do not follow links off these pages.
- Do not use Chrome or any other browser app.
- Do not open email, settings, or files outside this project.
- Prefer paraphrase; if you quote, keep quotes short.
- If a fact is unclear on the page, omit it — do not invent.

Steps:
1. Open each allowed URL and collect at most two short bullets from (1) and (2).
   From (3) only confirm you are on Wikipedia’s public portal (one short note).
2. Write slideshow.html in this project folder with exactly four full-viewport slides
   (simple inline CSS, no external scripts or fonts):
   - Slide 1 — Title: "CU Demo — Open Web Brief" / subtitle: "Draft — verify before trust"
   - Slide 2 — "What is AI?" (bullets from source 1)
   - Slide 3 — "What is an LLM?" (bullets from source 2)
   - Slide 4 — "Sources" (full URLs) + "Operator must verify before trust"
3. Open slideshow.html in the built-in browser, show slide 1, and stop.

End with: files written, which hosts needed permission, and one thing a malicious page could have tried if we had allowed arbitrary sites.
```

**While it runs — narrate out loud:**

| Moment | What you say |
|---|---|
| Site permission prompt | “This is a **host allow** — same family as app allow on Computer Use. I choose **once**, not forever.” |
| Agent reading the page | “Page text is **untrusted context**. Same instinct as poison intake — polish is not proof.” |
| Writing `slideshow.html` | “Deliverable hits **disk** in the project. Chat claim without a file is not evidence.” |
| Opening the deck | “Now we have something a supervisor might *feel* is done. That is the danger.” |

**Evidence the room must see:**

- [ ] Explorer: `slideshow.html` present  
- [ ] Browser: four slides advance (scroll or in-page anchors — whatever the file implements)  
- [ ] Slide 4 shows the real URLs  

**If it invents a third domain:** stop. Teaching moment: scope break.

**If it uses shell only and skips the browser:** stop or redirect once — “We named `@Browser` so the surface is visible. Shorter path is a contract miss.”

**Path B live prompt (only if preflight B is green):**

```text
@Browser Use only:
https://en.wikipedia.org/wiki/Artificial_intelligence
https://en.wikipedia.org/wiki/Large_language_model
Collect ≤2 short bullets each. No other links.

Then @Computer open PowerPoint and build a 4-slide deck:
1) Title CU Demo — Open Web Brief (Draft — verify before trust)
2) What is AI?
3) What is an LLM?
4) Sources (URLs) + Operator must verify before trust
Save as Open_Web_Brief.pptx in this project folder. Quit PowerPoint. Stop.
```

Narrate foreground takeover when PowerPoint is driven. Still open the file from disk to prove it.

### 22:00–26:00 — Verify + stop authority (required)

**Verify (2–3 min):**

1. Leave the deck on slide 2 or 3.  
2. Re-open source 1 or 2 in `@Browser` (or the same pages already open).  
3. Pick **one bullet** and match it to the page out loud.  
4. Mark one line verbally: **supported** / **soft paraphrase** / **kill**.  
5. Say: “This is P3/P5 energy on a pretty artifact. Agreement with the model is not the standard — the source is.”

**Stop beat (required even if the deck is pretty):**

Start a follow-up that would clearly continue:

```text
@Browser Expand this into 12 slides with more detail from the same two articles.
Add images if you can. Do not stop until all 12 exist.
```

When it begins navigating or writing again, **stop the task** from the Codex UI. Say:

> Stop authority is not a slogan from this morning. Unbounded “make the deck nicer” is how scope and spend die.  
> You interrupt, you own whether anything else is saved.

Optional: show Settings → Browser allow list and remove a host.

### 26:00–30:00 — Contract map + transfer seed

| Tool-ish / product-enforced | Procedure-enforced (you) |
|---|---|
| Browser / Computer Use plugin on or off | Whether this machine ever enables them |
| Per-site and per-app permission prompts | Allow once vs Always allow policy |
| Built-in browser profile ≠ your Chrome SSO | Closing real mail/SSO apps before any GUI run |
| Project sandbox on files/shell | Scoped URL allow-list in the brief |
| Cannot drive Codex itself / no UAC click-through | **Verify deck claims** before trust; stop runaway expands |

**Room prompt (pick one):**

1. Write one Transfer seed: *“I let an agent browse only when sources are ___ ; I accept a deck only when ___.”*  
2. Name one work artifact that should stay **pipeline + human gate** (P7) even if browser+deck works.  
3. What is more dangerous: a wrong text file, or wrong slide 2 in a leadership brief? Why?

**Close line:**

> P7 is the other machine: fixed path, human gate on exceptions. What you just saw is still an **agent** — browser, hands, and a pretty export. Do not confuse “it made slides” with “the line is true.”

Then open P7.

---

## What not to demo in this slot

- Chrome extension / `@Chrome` on a profile with real logins  
- “Allow for all sites” / always-allow browser content  
- Open-ended research with no URL allow-list  
- Banking, admin consoles, HR, production tickets, internal wikis  
- Parallel Computer Use tasks on the same app  
- macOS locked-use claims on a Windows projector  
- Store/native-host repair theater  
- Claiming this is required for course pass or pre-work GREEN

---

## Fallback script (Browser / Computer Use unavailable) — still 30 minutes

### Goal

Same vocabulary: scoped sources, collate to a deck, verify, stop — without fake GUI success.

### Flow

| Min | Beat |
|---|---|
| 0–5 | Frame + three-surface table + `browse ≠ verified` |
| 5–12 | Show plugin/settings failure honestly **or** “Browser tool missing in session” |
| 12–22 | **Manual collate:** lead opens the two Wikipedia URLs in a normal browser window (or local mirror); in Codex **without** browser tool, paste two short excerpts and ask only: “Turn these excerpts into slideshow.html with four slides…” then open the file in Explorer / default browser |
| 22–26 | Verify one bullet against the live page; discuss what the missing browser tool would have automated (and risked) |
| 26–30 | Same contract map + transfer seed |

**Fallback collate prompt (no browser tool):**

```text
Using ONLY the excerpts I paste below (no other knowledge), write slideshow.html
in this project with four full-viewport slides: Title, AI, LLM, Sources.
Mark any gap as UNKNOWN rather than inventing.
Excerpts:
---
[paste]
---
```

Say:

> When the browser surface is dead, you still own scoped intake and a verify step. The course does not depend on Computer Use for GREEN — this slot is literacy, not a gate.

---

## Optional student stretch (after class — not Thursday PM bar)

Only if staff green-lights a healthy machine:

1. Disposable folder project  
2. **Two named public URLs only** + `@Browser`  
3. Four-slide `slideshow.html` (no Chrome extension)  
4. Log: hosts allowed, one verified bullet, one killed or softened bullet, how you stopped  

PowerPoint path remains staff-optional only.

---

## Facilitator checklist (print or pin)

**Before lunch Thu**

- [ ] Cold smoke Path A passed (HTML deck)  
- [ ] Path B only if PPTX + Computer Use both green — else leave it  
- [ ] `cu-demo` clean; secrets apps quit  
- [ ] Source URL list fixed; fallback excerpts copied if network is hostile  
- [ ] Stop-beat prompt in clipboard  

**During**

- [ ] Students do not install Browser/Computer Use/Chrome  
- [ ] Site allow = once (narrated)  
- [ ] Deck opened from disk, not only described in chat  
- [ ] At least one claim verified against source  
- [ ] Stop beat executed once  
- [ ] Transfer seed spoken  

**After**

- [ ] Revoke demo site Always allows you do not want  
- [ ] Note cohort log: Path A / Path B / Fallback + one flake line if any  

---

## Why this sits after lunch (geometry)

- **Morning P6** built contract language and stop authority.  
- **Case talk before lunch** was a lived autonomy story.  
- **After lunch** shows a seductive multi-step agent: **web → polished deck** — then P7 teaches the other machine (pipeline + gate).  
- Lead-only protects clinic/GREEN from Windows plugin flake and from twenty Chrome profiles with real SSO.

---

## Source truths baked into this script (re-verify if product moves)

- Built-in browser vs Chrome extension; site allow/block; treat page content as untrusted.  
- Computer Use: app approvals, Windows foreground, no terminal/ChatGPT automation, no UAC click-through.  
- Course MEMORY: API keys only; Computer Use/plugins limited → lead demo / stretch never MVP; no student Chrome setup.
