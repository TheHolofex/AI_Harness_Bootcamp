# Module 0 · Set up the harness and direct bounded work

Plan for 1–3 hours of machine setup. Setup is finished only after you reopen the terminal and the tools still work. You will watch each AI tool write a real file, then use the same setup to draft and check a short email against a supplied set of facts.

## Start here

Choose one command-line path and stay in it. A shell is the text window that runs the commands you paste.

| Your machine | Use this guide |
|---|---|
| Windows, no Linux shell | [Windows · PowerShell only](platforms/windows-powershell.md) |
| Windows with or willing to install WSL 2 | [Windows · WSL 2 with Ubuntu](platforms/windows-wsl.md) |
| Mac | [macOS](platforms/macos.md) |
| Ubuntu desktop | [Ubuntu](platforms/ubuntu.md) |
| Arch Linux desktop | [Arch Linux](platforms/arch-linux.md) |

If you are unsure which Windows path to use, choose WSL when your organization permits it and you are comfortable restarting the machine. Choose PowerShell when WSL is blocked or you need a native Windows-only environment. Do not complete both.

## What you will install

- Git and a copy of this course (a repository: a folder Git can version).
- Node.js 24 LTS and npm
- Python 3.12 or newer
- Codex command-line tool (CLI)
- OpenCode 1.18.17
- goose CLI from the Agentic AI Foundation
- n8n 2.34.5
- Obsidian

The AI CLIs make short provider-billed proof calls. Before you enter any credential, ask whoever owns your AI provider accounts which account, provider, and model to use.

## Before the first command

- Reserve a restart window.
- Connect to a stable network.
- Keep at least 15 GB free; WSL should have 25 GB.
- Have administrator approval for operating-system packages.
- Keep credentials in the approved password manager or secure handoff.
- **Do not paste a key into a command, Markdown file, shell profile, screenshot, ticket, or repository.**
- If a managed laptop says that policy blocks a step, stop and save the exact message for whoever supports your machine.
- If you use a screen reader, keyboard-only navigation, magnification, voice control, or another access method, read [Accessibility and equivalent operation](shared/ACCESSIBILITY.md) first.

## When a step fails

Save the first error message before you change anything, then work from [When setup stops](shared/TROUBLESHOOTING.md). Change one thing, and run the check that failed again.

![Save the first error, change one thing, rerun](shared/figures/m00-recovery.svg)

*Save the first error, change one thing, and rerun the same check.*

<details>
<summary>Figure text</summary>

Save the first error message. Change one thing. Run the same check again.

</details>

## Ready means observable

Setup is finished when a terminal you opened after the last install shows these values:

![Setup is finished only after a new terminal proves it](shared/figures/m00-setup-chain.svg)

*Read each proof file from a terminal you opened after the last install.*

<details>
<summary>Figure text</summary>

Install the tools. Authenticate. Open a new terminal. Read each proof file from disk. A tool saying done is not the same as a file on disk.

</details>

- `origin` reporting `https://github.com/TheHolofex/AI_Harness_Bootcamp.git`, `git rev-parse HEAD` reporting a 40-character id (the setup check prints the first 12), and `git status --short` printing nothing at all;
- `node --version` printing a version that starts with `v24.`, and Python reporting 3.12 or higher (macOS uses `python3.12 --version`; Ubuntu, Arch, and WSL use `python3 --version`; PowerShell-only uses `python --version`);
- `opencode --version` and `n8n --version` printing the pinned versions listed above;
- the Codex and goose version strings, and the absolute path each command resolved to, as printed by the setup check;
- `codex login status` finishing without an error, with no account detail copied anywhere;
- the word `SET` from the key check in that same terminal — macOS prints it as `XAI_API_KEY=SET` — and the key value itself printed nowhere;
- three proof files read back from disk, each one written by the tool that claimed to write it;
- `PASS: n8n answered its health check at http://127.0.0.1:5678`;
- the course files listed in Obsidian's file pane, and `git status --short` still printing nothing after you close it;
- the same absolute tool paths and the same file-writing results you saw in the terminal where you installed everything; and
- a setup report saved outside the Git clone with no key, token, or password in it.

The setup check reports each of these as PASS with the value it observed, WARN when the value is outside the expected set but the work can go on, or FAIL when the value blocks later work.

Open each proof file and read it back before you accept it: a tool saying “done” is not the same as a file on disk.

## After setup

Put the machine to work: [Give AI a clear, limited job](shared/MODULE_00_LAB.md).
