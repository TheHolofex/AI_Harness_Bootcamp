# Pre-work module — Mission workstation

This module gets **your** Windows laptop ready for the bootcamp.
You install and set up the tools yourself — there is no golden image and no "IT hands you a finished laptop."

That is deliberate. At work you will own the chair the thinking machine sits in. Pre-work is Cap 0: stand up the workstation before mission week begins. Plan a focused evening or weekend block — often two to four hours, depending on your machine and how much your IT policy pushes back.

## When

Complete **before Monday Block 0**. Do not start pre-work in the Monday morning contact window — that time is for First Light, not install.

## Everything runs on API keys

Staff issue you **three API keys**: OpenAI, xAI, and Anthropic. You will never sign into ChatGPT, Claude, or any monthly subscription during this course.

This matters at the keyboard, because several tools in the stack offer a subscription login and an API key option on the same screen. Always take the API key path. See `site/keys.html` for what each key drives, how to store it, and what to do if one leaks.

Keys are prepaid and carry a spending cap. A tool that worked yesterday and fails today with a `429` or a quota message has hit the cap rather than broken — that is a staff fix, not a reinstall.

## What "done" means

You can prove all of the following on **your** Windows 11 machine:

1. Required tools installed and configured against your keys
2. Each major setup step’s **verify** checks passed (fresh terminal after PATH changes)
3. All **four required** agents wrote a real file into a temp project folder you can see in Explorer
4. You bring a **setup log** — what broke, what you fixed

There is **no separate health-check pass**. Monday AM is an **install clinic** (~2 hours expected, no hard wall) to finish gaps under staff eyes, then First Light. Clinic is finish-and-prove — not a substitute for skipping pre-work.

## Required stack (vanilla Windows 11, 64-bit — no WSL)

| # | Component | Notes |
|---|---|---|
| 1 | Windows 11, 64-bit | **Not ARM64** — OpenCode and goose have no working ARM build |
| 2 | Git for Windows | Provides Git Bash, which Pi requires. Students still work in **PowerShell** — Git Bash is a dependency, not a second shell to learn |
| 3 | Node.js **LTS** | Use the `OpenJS.NodeJS.LTS` package id — must land in 22.22–24.x |
| 4 | Python 3.x | |
| 5 | PowerShell execution policy | `RemoteSigned` for CurrentUser, and no Group Policy override |
| 6 | **Three API keys** | OpenAI · xAI · Anthropic, stored as Windows user variables |
| 7 | **Codex app** | Primary home all week · Codex mode in the **ChatGPT desktop app**, from the Microsoft Store · sign in via *Sign in another way* |
| 8 | **OpenCode** | **Required second engine** · runs Grok on your xAI key · use the cohort-pinned version · set `OPENCODE_DISABLE_CLAUDE_CODE=1` so it doesn't read Claude Code's files |
| 9 | **Pi** | Minimal harness you extend · multi-provider · needs Git Bash · pin the model explicitly · **no sandbox and no working-directory fence** |
| 10 | **goose** | Local agent platform · recipes + extensions + permission modes + schedule · CLI required, Desktop optional · from `aaif-goose`, **not** winget · docs: goose-docs.ai |
| 11 | **Obsidian** | Local vault, no account |
| 12 | **n8n** | Local install · owner account is local-only, not a subscription |

### Optional

| Component | Notes |
|---|---|
| **Claude Code** (CLI) | Alternate third engine — **not** required for GREEN or course pass. Use the command-line tool; the Claude desktop app's Code tab needs a subscription and will not accept your key. |

## How to run pre-work

1. Prefer the **interactive site checklist** (primary path):
   - Keys reference: `site/keys.html`
   - Install + verify as you go: `site/checklists/prework-install.html`
2. Or work `INSTALL_GUIDE.md` top to bottom and fill in `SETUP_LOG.md`.
3. Stop when each section’s verify is true — do not plan a second full “health check” pass.
4. Bring laptop and setup log to Monday clinic.

## Twin-engine note

During the week, **P3 Twin-engine** runs the same frozen brief on:

1. **Codex** on your OpenAI key
2. **OpenCode** on your xAI key (Grok)

That is the required comparator pair. Claude Code is welcome as an optional extra mind, not a substitute for OpenCode unless staff waive it for a documented install failure.

The pair only tells you something if the two engines are genuinely separate, and both of them load context you never typed. OpenCode reads `~/.claude/CLAUDE.md` and `.claude/skills` when it finds them, which is why step 8 sets `OPENCODE_DISABLE_CLAUDE_CODE=1`. The Codex app loads `AGENTS.md`, skills, and memories from wherever you run it. Neither announces what it picked up. You will handle the Codex side during P3 itself; the install-time half is step 8.

## Known traps worth reading before you start

These cost the most time, and none of them announce themselves clearly:

- **A new terminal is required after every install.** A terminal reads PATH once when it opens. This causes more "it didn't install" reports than everything else combined.
- **The Codex app ignores `OPENAI_API_KEY` entirely.** Every other tool reads the variable; this one reads the key you paste into *Sign in another way* on its signed-out screen. Take that path, not the ChatGPT account button beside it.
- **The permission mode is what switches the sandbox on.** Set it to **Ask for approval** beneath the message box. Left unset, Codex works without the boundaries the rest of the week depends on.
- **The `.LTS` suffix on the Node package id is not optional.** Plain `OpenJS.NodeJS` installs a release too new for n8n.
- **`winget install ... goose` is a different program** — an unrelated database tool with the same name. Install from `aaif-goose` only.
- **goose is more than a one-shot CLI.** Thursday’s contract uses its recipe, tool surface, mode/max-turns dial, and schedule path — pre-work only proves install + one write.
- **OpenCode's `curl` install command cannot run on Windows PowerShell.** It is a bash script; no PowerShell equivalent exists.
- **OpenCode reads Claude Code's files by default.** `~/.claude/CLAUDE.md` and `.claude/skills` load into your second engine unless you set `OPENCODE_DISABLE_CLAUDE_CODE=1`. Nothing warns you; the comparison just gets quieter.
- **Pi finds its shell lazily**, so a missing Git Bash fails mid-exercise rather than at setup. Test it during install.
- **Pi has no working-directory fence.** No sandbox, no approval prompt, and an absolute path or `~` reaches anything your account can. Staying in the smoke folder is a convention you keep, not a boundary Pi enforces.
- **n8n's first screen looks like a signup and is not one** — it creates a local account on your own laptop.

## Support rules

- Pre-work support window: [course fills channel/hours].
- Post the step number, the exact error text, and what you already tried. Then move to the next section while you wait — most are independent.
- "I didn't start until Sunday night" is not a clinic delay the whole room will wait on.
- Corporate-locked machines and ARM64 laptops: escalate early. Neither is fixable from your seat.

## Identity lock

Skipping pre-work to "just use a lab image" is not this school.
Owning install pain once is cheaper than never owning the workstation.

A recorded failure is evidence, not shame.
