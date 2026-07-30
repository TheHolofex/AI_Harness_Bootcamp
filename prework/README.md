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
2. Health check GREEN (or YELLOW with a documented workaround)
3. All **four required** agents wrote a real file into a temp project folder
4. You bring a **setup log** — what broke, what you fixed

Monday Block 0 **verifies** this gate, then moves to First Light. It does not install the stack from zero for the room.

## Required stack (vanilla Windows 11, 64-bit — no WSL)

| # | Component | Notes |
|---|---|---|
| 1 | Windows 11, 64-bit | **Not ARM64** — OpenCode and goose have no working ARM build |
| 2 | Git for Windows | Provides Git Bash, which Pi requires |
| 3 | Node.js **LTS** | Use the `OpenJS.NodeJS.LTS` package id — must land in 22.22–24.x |
| 4 | Python 3.x | |
| 5 | PowerShell execution policy | `RemoteSigned` for CurrentUser, and no Group Policy override |
| 6 | **Three API keys** | OpenAI · xAI · Anthropic, stored as Windows user variables |
| 7 | **Codex** | Primary home all week · `codex login --with-api-key` |
| 8 | **OpenCode** | **Required second engine** · runs Grok on your xAI key · use the cohort-pinned version |
| 9 | **Pi** | Bare loop · needs Git Bash · pin the model explicitly |
| 10 | **goose** | Bounded autonomy and recipes · from `aaif-goose`, **not** winget |
| 11 | **Obsidian** | Local vault, no account |
| 12 | **n8n** | Local install · owner account is local-only, not a subscription |

### Optional

| Component | Notes |
|---|---|
| **Claude Code** (CLI) | Alternate third engine — **not** required for GREEN or course pass. Use the command-line tool; the Claude desktop app's Code tab needs a subscription and will not accept your key. |

## How to run pre-work

1. Prefer the **interactive site checklists** (primary path):
   - Keys reference: `site/keys.html`
   - Install: `site/checklists/prework-install.html`
   - Health gate: `site/checklists/prework-health.html`
2. Or work `INSTALL_GUIDE.md` top to bottom and fill in `SETUP_LOG.md`.
3. Run the health check until you can declare a colour honestly.
4. Bring laptop and setup log to Monday.

## Twin-engine note

During the week, **P3 Twin-engine** runs the same frozen brief on:

1. **Codex** on your OpenAI key
2. **OpenCode** on your xAI key (Grok)

That is the required comparator pair. Claude Code is welcome as an optional extra mind, not a substitute for OpenCode unless staff waive it for a documented install failure.

## Known traps worth reading before you start

These cost the most time, and none of them announce themselves clearly:

- **A new terminal is required after every install.** A terminal reads PATH once when it opens. This causes more "it didn't install" reports than everything else combined.
- **`OPENAI_API_KEY` alone does not authenticate Codex.** It only pre-fills the sign-in screen. Codex needs `codex login --with-api-key` once.
- **The `.LTS` suffix on the Node package id is not optional.** Plain `OpenJS.NodeJS` installs a release too new for n8n.
- **`winget install ... goose` is a different program** — an unrelated database tool with the same name.
- **OpenCode's `curl` install command cannot run on Windows PowerShell.** It is a bash script; no PowerShell equivalent exists.
- **Pi finds its shell lazily**, so a missing Git Bash fails mid-exercise rather than at setup. Test it during install.
- **n8n's first screen looks like a signup and is not one** — it creates a local account on your own laptop.

## Support rules

- Pre-work support window: [course fills channel/hours].
- Post the step number, the exact error text, and what you already tried. Then move to the next section while you wait — most are independent.
- "I didn't start until Sunday night" is not a Block 0 content delay.
- Corporate-locked machines and ARM64 laptops: escalate early. Neither is fixable from your seat.

## Identity lock

Skipping pre-work to "just use a lab image" is not this school.
Owning install pain once is cheaper than never owning the workstation.

A recorded failure is evidence, not shame.
