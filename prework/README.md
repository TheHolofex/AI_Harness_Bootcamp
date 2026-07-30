# Pre-work module — Mission workstation

This module gets **your** Windows laptop ready for the bootcamp.  
You install and set up the tools yourself — there is no golden image and no “IT hands you a finished laptop.”

That is deliberate. At work you will own the chair the thinking machine sits in. Pre-work is Cap 0: stand up the workstation before mission week begins. Plan for a focused evening or weekend block (often about 2–4 hours, depending on your machine and accounts).

## When

Complete **before Monday Block 0**. Do not start pre-work in the Monday morning contact window — that time is for First Light, not install.

## What “done” means

You can prove all of the following on **your** Windows 11 machine:

1. Required tools installed and signed in / configured  
2. Health check GREEN (or YELLOW with documented workaround)  
3. All **four required** agents can read/write a temp project folder  
4. You bring a **setup log** (what broke, what you fixed)

Monday Block 0 **verifies** this gate, then moves to First Light.  
It does not install the stack from zero for the room.

## Required stack (vanilla Windows 11 — no WSL required)

| # | Component | Notes |
|---|---|---|
| 1 | Windows 11 | Prefer fully updated |
| 2 | Git for Windows | Git Bash on PATH (Pi and some agent paths need it) |
| 3 | Node LTS | via `winget` or official installer |
| 4 | Python 3.x | via `winget` or official installer |
| 5 | PowerShell execution policy | User-level `RemoteSigned` is typical |
| 6 | **OpenAI Codex app** | Primary home all week · signed in · native Windows agent |
| 7 | **OpenCode** | **Required second engine** · configure **Grok** (or course-pinned model) |
| 8 | **Pi** | Configured against Git Bash per pi.dev Windows docs |
| 9 | **goose** | Desktop and/or CLI · one sample recipe runs once |
| 10 | **Obsidian** | Installed (vault arrives in class) |
| 11 | **n8n** | Local install or approved class path |

### Optional

| Component | Notes |
|---|---|
| **Claude Code** (Desktop Code tab or CLI) | Alternate / third engine only — **not** required for GREEN or course pass |

Accounts, licenses, and API/seat access are issued by the course separately — install still fails closed without them.

## How to run pre-work

1. Prefer the **interactive site checklists** (primary path):  
   - Install: `site/checklists/prework-install.html`  
   - Health gate: `site/checklists/prework-health.html`  
2. Or work `INSTALL_GUIDE.md` top to bottom and tick `SETUP_LOG.md`.  
3. Run health check until green.  
4. Bring laptop + setup log to Monday.

## Twin-engine note

During the week, **P3 Twin-engine** runs the same frozen brief on:

1. **Codex app** (home)  
2. **OpenCode** (second harness — typically Grok)

That is the required comparator pair. Claude Code is welcome as an optional extra mind, not a substitute for OpenCode unless staff waive OpenCode for a documented install failure.

## Support rules

- Pre-work support window: [course fills channel/hours].  
- “I didn’t start until Sunday night” is not a Block 0 content delay.  
- Corporate-locked machines: escalate early.

## Identity lock

Skipping pre-work to “just use a lab image” is not this school.  
Owning install pain once is cheaper than never owning the workstation.
