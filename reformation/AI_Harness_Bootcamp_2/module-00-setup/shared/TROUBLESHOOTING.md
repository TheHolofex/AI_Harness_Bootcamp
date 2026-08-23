# When setup stops

Start with the first check that failed. Save its error message before you change anything, and do not reinstall everything.

## 1. Find the first failed check

| What you observed | Do this first |
|---|---|
| The package manager command is missing | Open the terminal your platform guide names, not another one, and run its version command: `brew --version`, `winget --version`, `apt --version`, or `pacman --version`. If it still reports "not found", the package manager is absent or blocked by policy; save the exact message and use the support packet. |
| The installer finished, and the command is still missing | Open a new terminal and run `command -v <tool>` — `Get-Command <tool>` in PowerShell. Empty output means the folder holding the tool is not on PATH. Redo the "Put user tools on PATH" step in your platform guide, then open another new terminal and run `command -v <tool>` again. |
| The command runs and authentication fails | Run `codex login status` and compare the reported method against the one whoever owns the account told you to use. If that is right, check the provider name, the model ID, and whether the key is set in this process. A corporate proxy shows up as a timeout or a certificate error, not as a rejected credential. |
| The AI tool answers and no file appears | Run `pwd` and `ls` — `Get-Location` and `Get-ChildItem` — in the folder you told the tool to write into, and open any file it lists. If the folder is empty, run the tool again from inside that folder and watch for a permission prompt you dismissed. |
| The file appears in the wrong place | Print the working directory before you run the tool again. On Windows with WSL, a path starting `/mnt/c/` means a Linux command wrote to the Windows disk; the course clone belongs under your Linux home. |
| The old terminal works and a new one fails | The setting exists only in the old process. Put it in the shell profile your platform guide names, then prove it in a third terminal you open afterwards. |
| A new shell finds the tools but not the xAI key | Expected. The course key is session-only. Enter it again with the hidden-input step in your platform guide. |
| A step has printed nothing for far longer than your guide said it would take | Do not press Ctrl+C yet, and do not close the window. Work through "When a step goes silent" below: find out whether the machine is still doing the work before you interrupt it. |
| Output stopped, the screen is full, and the bottom line shows `:` or `(END)`, and what you type does not appear | A pager is showing you a file — `less` on macOS and Linux, `more` on Windows. Press `q` to return to the prompt. Nothing was cancelled and nothing was installed by looking. `Space` moves down a page, `b` moves back. |
| Windows says "running scripts is disabled on this system" | PowerShell is refusing to run a `.ps1` file. Run `Get-ExecutionPolicy -List`. If `MachinePolicy` or `UserPolicy` shows any value, IT controls this: stop, send them that output, and do not weaken it. If both are `Undefined`, use the scoped change named in the PowerShell guide and record the old value first. |
| A downloaded Linux application will not start | Start it from the terminal so you can read the error instead of double-clicking. For an AppImage: `chmod +x` the file first; "AppImages require FUSE to run" means installing `libfuse2` — `libfuse2t64` on Ubuntu 24.04 and later — or running the file once with `--appimage-extract-and-run`. If there is no message at all, run `echo "$DISPLAY$WAYLAND_DISPLAY"`; empty output means no desktop session, and a desktop application cannot open there. |
| n8n will not start, or the n8n check reports that something else is listening on port 5678 | Find what holds the port: `lsof -i :5678` on macOS, `ss -ltnp 'sport = :5678'` on Linux, `Get-NetTCPConnection -LocalPort 5678` in PowerShell. Usually it is an earlier `n8n start` still running or a leftover container. Stop that process and start n8n again. Do not move n8n to another port; the check reads 5678. |
| A download fails with certificate or proxy text | A network or proxy setting, not a broken download. Retry on a different network if you can, and send the exact text to IT. Do not disable TLS verification. |
| `permission denied` under npm | The global npm folder is not yours. Run `npm config get prefix`; it must be a folder inside your home directory. Redo the npm prefix step. Do not add `sudo`. |
| WSL work is slow under `/mnt/c` | Cross-filesystem access is the cost. Move the clone into the Linux home directory and work there. |
| An Arch package transaction reports conflicts | Stop and resolve a full system upgrade with `pacman -Syu` before installing anything else. Syncing the database without the upgrade leaves a mismatched system. |

**PATH is the list of folders your terminal searches, in order, when you type a command name.** If the folder an installer wrote to is not in that list, the file exists on disk and the command still reports "not found" — which is why an installer can report success and the tool still be missing. Each platform guide's PATH step adds the folder and writes it into your shell profile so that terminals you open later inherit it. A terminal opened before that change keeps the old list until you close it and open a new one.

### When a step goes silent

Your platform guide gives each slow step a duration and tells you a minute of silence inside one is normal. Here is where silence stops being normal. Treat these as estimates from ordinary machines and connections, not as measurements of yours:

- a package download or install the guide sizes at 5 to 20 minutes: about 30 minutes with nothing new on screen;
- a full Arch upgrade, sized at 5 to 40 minutes: about an hour;
- a first `n8n start`, sized at 1 to 3 minutes: about 10 minutes;
- anything the guide does not call slow: about 5 minutes.

Two questions separate a slow step from a stuck one. Answer both from a second terminal window, because the running command holds the first.

**First: does the process still exist?**

**Terminal: a second window of the terminal your platform guide names · normal user.**

```bash
pgrep -a -f 'apt|dpkg|pacman|brew|npm|node|curl|wget'
```

**PowerShell:**

```powershell
Get-Process node, npm, winget, curl, msiexec -ErrorAction SilentlyContinue | Format-Table Name, Id, CPU
```

**You should see:** one line for each matching process, with the command it is running. No lines at all means the command has already ended — go back to the first window and press Return to see whether the prompt is back.

**Second: is the machine still working for it?** Run the command above again a minute later. In PowerShell the `CPU` column counts seconds of processor time, so a number that has grown means work is happening. Elsewhere, open Activity Monitor on macOS, System Monitor or `top` on Linux, or Task Manager on Windows, find the process by name, and read its CPU, disk and network figures twice a minute apart. Figures that move mean a slow step. Figures at zero in both readings mean a stuck one. For a download, running `ls -l` — `Get-ChildItem` — in the folder twice a minute apart answers the same question: a file whose size is growing is still arriving.

When it is stuck, press Ctrl+C in the first window, save the last lines it printed, and run the same command again; package installs and npm pick up where they left off, and a second run usually gets past a dropped connection. If it stops at the same point twice, that point is your first error: capture the packet below and stop there.

## 2. Capture a support packet

Save this without secrets:

```text
Platform and version:
Architecture:
Terminal and privilege level:
Current directory:
Step title:
Command or UI action:
Exact first error:
What you expected:
What changed immediately before it:
Can the prior checkpoint still pass? yes / no / unknown
```

For command output, redact usernames, organization names, account IDs, internal hosts, and tokens. Do not redact the command name, exit code, package version, or first error line.

## 3. Make one correction

Change only the setting or tool named by the error, then rerun:

1. the failed check;
2. the preceding known-good check; and
3. the fresh-shell check if PATH or the environment changed.

If the correction fails, undo it before trying another. Stop after two unsuccessful corrections, an undo that fails, or a message controlled by company policy. Record `HOLD` and send the saved details to whoever supports your machine.

## Do not use these shortcuts

- `curl -k`, `--insecure`, or disabling certificate checks;
- machine-wide execution-policy weakening;
- disabling Gatekeeper or antivirus;
- installing global npm packages with `sudo`;
- `chmod -R 777`;
- deleting an existing course folder without inspecting or backing it up;
- moving WSL work onto the Windows filesystem to make paths look familiar;
- pasting a key into a support ticket.
