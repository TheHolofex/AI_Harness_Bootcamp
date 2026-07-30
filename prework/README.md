# Pre-work module — Mission workstation

This module gets **your** Windows laptop ready for the bootcamp.  
You install and set up the tools yourself — there is no golden image and no “IT hands you a finished laptop.”

That is deliberate. At work you will own the chair the thinking machine sits in. Pre-work is Cap 0: stand up the workstation before mission week begins. Plan for a focused evening or weekend block (often about 2–4 hours, depending on your machine and accounts).

## When

Complete **before Monday Block 0**. Do not start pre-work in the Monday morning contact window — that time is for First Light, not install.

## What “done” means

You can prove all of the following on **your** Windows 11 machine:

1. Required tools installed and signed in  
2. Health check script (or checklist) passes  
3. All four agents can read/write a temp project folder  
4. You bring a one-page **setup log** (what broke, what you fixed)

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
| 7 | **Claude Desktop** with **Code** tab | Second engine · signed in · Git available |
| 8 | **Pi** | Configured against Git Bash per pi.dev Windows docs |
| 9 | **goose** | Desktop and/or CLI · one sample recipe runs once |
| 10 | **Obsidian** | Installed (vault arrives in class) |
| 11 | **n8n** | Local install or approved class path (see detailed guide) |

Accounts, licenses, and API/seat access are issued by the course separately — install still fails closed without them.

## How to run pre-work

1. Open `prework/INSTALL_GUIDE.md` and work top to bottom.  
2. After each major install, record result in `prework/SETUP_LOG.md` (copy into your machine).  
3. Run `prework/HEALTH_CHECK.md` until green.  
4. Export or screenshot health-check proof into your setup log.  
5. Bring laptop + setup log to Monday. Optional: zip log into the class drop.

## Support rules

- Pre-work support window: [course fills channel/hours].  
- “I didn’t start until Sunday night” is not a Block 0 content delay — use rescue path in the guide.  
- Corporate-locked machines: escalate early; some sandbox/firewall steps need admin.

## Identity lock

Skipping pre-work to “just use a lab image” is not this school.  
Owning install pain once is cheaper than never owning the workstation.
