# Accessibility and equivalent operation

You must be able to perform the same action and observe the same state as anyone else on this setup path. Operate each control with your own access method, and read the value it produces yourself. Where a control cannot be operated with your access method, the honest outcome is a recorded `HOLD` and a support request, not a demonstration someone narrates to you.

Nothing here is timed. A check does not become a `FAIL` because reaching it took longer.

## What you can rely on

- Every command is selectable text, never an image.
- Each command block names the terminal and the privilege level before the command.
- Results are words — `PASS`, `WARN`, `FAIL`, `HOLD` — and no result is carried by color alone.
- Browser zoom, terminal font size, contrast, and reduced-motion settings change nothing a check reads.

## Terminal work with a screen reader

The terminal is the most accessible part of this setup: it is text, it stays in one place, and every result is a printed value you can re-read. VoiceOver on macOS, Narrator, NVDA or JAWS on Windows, and Orca on Linux all announce that text line by line as it arrives. Two things follow from line-by-line announcement.

An install that prints several hundred lines will be read to you for as long as it prints, and silencing speech does not stop the command. Let it finish, then read the last lines.

Scrollback is awkward to review under any screen reader, so send long output to a file and read it in your editor, where you can move by line and search. Add the redirection to the end of the command.

**Terminal: the terminal named by your platform guide · normal user.**

```bash
node --version > "$HOME/setup-output.txt" 2>&1
```

**PowerShell:**

```powershell
$out = Join-Path $env:USERPROFILE 'setup-output.txt'
node --version *> $out
```

The `2>&1` and `*>` forms capture error text as well, which is the part you usually need. The setup check already writes its own report to a file; read that file rather than the screen.

## Opening the course folder as an Obsidian vault

Obsidian's own documentation gives the pointer route: the vault profile icon at the bottom left, then **Manage vaults…**, then **Open folder as vault**, then the course folder.

From the keyboard, `Ctrl+P` — `Cmd+P` on macOS — opens Obsidian's command palette. Type `Open another vault`, move to it with the arrow keys, and press `Enter`. That reaches the same vault window that carries **Open folder as vault**. Obsidian documents the palette shortcut and the `Open another vault` command; it publishes no keyboard or screen-reader documentation for the vault window itself, and whether its **Open** button is reachable and announced is unverified. Treat that one control as unverified: if it does not respond to your access method, that is a known gap, not something you are doing wrong.

The folder chooser that opens next is your operating system's own dialog — Finder, the Windows file dialog, or your Linux desktop's file chooser — so it behaves as it does in every other application on your machine.

The value that settles this step is visible from the terminal. Opening a folder as a vault makes Obsidian create a configuration folder named `.obsidian` inside that folder, so you do not have to read the Obsidian window to know it worked.

**Terminal: the terminal named by your platform guide · normal user.**

```bash
ls -d "$HOME/course/AI_Harness_Bootcamp/.obsidian"
```

**You should see:** the path printed back to you. On the WSL path, run this in the Ubuntu terminal even though Obsidian is running on Windows.

**PowerShell:**

```powershell
Test-Path -LiteralPath (Join-Path $env:USERPROFILE 'course\AI_Harness_Bootcamp\.obsidian')
```

**You should see:** `True`.

If the vault window will not respond to your access method, stop at that step, record `HOLD`, and send the support request below. Do not record a pass for a control you did not operate.

Sources: [Obsidian · Manage vaults](https://obsidian.md/help/manage-vaults), [Obsidian · Command palette](https://obsidian.md/help/plugins/command-palette), [Obsidian · Configuration folder](https://obsidian.md/help/configuration-folder).

## Reaching the local n8n page

To settle whether n8n is running, run the n8n check your platform guide names. It asks n8n's own health endpoint from the terminal and prints:

```text
PASS: n8n answered its health check at http://127.0.0.1:5678
```

On four of the five setup paths that line is the whole requirement, and nothing asks you to open the editor or build a workflow.

The WSL path adds one browser step, for a different question: can Windows reach the service running inside Ubuntu? In Chrome, Edge and Firefox on Windows, `Ctrl+L` moves focus to the address bar; type `localhost:5678` and press `Enter`. If your access method cannot tell you whether that page loaded, ask Windows the same question in text and read the number it prints.

**PowerShell:**

```powershell
(Invoke-WebRequest -UseBasicParsing 'http://localhost:5678/healthz').StatusCode
```

**You should see:** `200`. Windows reached n8n inside Ubuntu, which is everything the browser step was asking.

Inside the n8n editor, n8n documents one keyboard entry point, a command bar on `Ctrl+K` (`Cmd+K` on macOS). Beyond that it publishes no screen-reader or keyboard-accessibility documentation, and open reports on n8n's issue tracker describe the workflow canvas as unusable without a pointer. You are never asked to work in that canvas here, so stop at the value above and close the page.

Source: [n8n · Keyboard shortcuts](https://docs.n8n.io/build/keyboard-shortcuts).

## Equivalent paths

An equivalent path must expose:

1. the same input files;
2. the same resolved configuration and authority;
3. the same run, stop, and restore actions;
4. the same raw output and check result; and
5. the same opportunity to make the decision.

If the native interface is inaccessible and no equivalent path meets all five conditions, record `HOLD`. Do not replace operation with a narrated demonstration.

## Support request

Send whoever is helping you enough to reproduce the block without a second round of questions:

```text
Platform and setup path:
Access method, with versions (screen reader, keyboard only, magnification, voice control):
Application and version where the block happens:
Step title, and the exact command or control:
What you expected to hear or see:
What was announced or displayed instead:
What the terminal check printed, if one ran:
Alternatives already tried, and what each one did:
Which outcome would unblock you:
How and when to reach you:
```

Do not include medical details, a diagnosis, or credentials. None of that helps anyone fix a control.
