# Windows · WSL 2 with Ubuntu

Windows stays the desktop. Every command-line course tool runs inside Ubuntu on WSL 2, a real Linux system that runs alongside Windows on the same machine. Reserve 2 to 3 hours if WSL is new, because installing it restarts the computer.

Two systems means two kinds of command. Every block below names its terminal before the first command: Windows PowerShell, or Ubuntu. Nothing in this path asks you to type a Windows command into Ubuntu or a Linux command into PowerShell.

Keep the repository in the Linux home directory. A Windows copy and a Linux copy of the same files drift apart and are hard to tell apart afterwards. Open those Linux files from Windows desktop applications such as Obsidian, and install Node, Git, Python, Codex, OpenCode, and goose only inside Ubuntu, even if Windows already has a version of one of them.

## 1. Before you change the machine

Installing WSL changes the machine and needs administrator rights, so check the machine can take it first.

**Terminal: Windows PowerShell · Run as administrator.** Right-click the Start button and choose **Terminal (Admin)**, or **Windows PowerShell (Admin)**.

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber, OsArchitecture
Get-PSDrive -Name C | Select-Object Name, @{Name='FreeGB';Expression={[math]::Round($_.Free/1GB,1)}}
wsl --status
wsl --list --verbose
```

**You should see:** `OsBuildNumber` of 19041 or higher. That covers Windows 10 version 2004 and later, and every Windows 11 build, which start at 22000. `FreeGB` reads 25 or more; that number is the free space left on the C drive, not its total size. `OsArchitecture` reads `64-bit` or `ARM 64-bit`, and both can start this path. WSL either prints its status or reports that it has no installed distributions.

**Stop here if:** `OsBuildNumber` is below 19041, `FreeGB` is below 25, virtualization is disabled, organizational policy blocks WSL, or you cannot schedule a restart. Installing WSL needs administrator approval. If policy blocks it, stop and send the message to IT; do not install an unofficial substitute.

Source: [Microsoft Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install).

## 2. Open the right terminal

If `wsl --list --verbose` did not show Ubuntu, install WSL and the default Ubuntu distribution now.

**Terminal: Windows PowerShell · Run as administrator.**

Expect this to take 10 to 30 minutes on a normal connection, **and the machine restarts partway through**. Save and close your other work before you run it. It prints download percentages and component names, then asks to restart Windows. A minute or two with no new output is normal.

```powershell
wsl --install
```

**Restart Windows when it asks.** Nothing further works until you do.

After the restart, Ubuntu finishes installing and opens on its own. If it does not, open **Ubuntu** from the Start menu. Ubuntu then asks for a new username and password for the Linux system; these are separate from your Windows account. The password does not appear while you type — no characters, no dots, no stars. That is normal terminal behavior, not a frozen prompt. Type it, press Enter, then type it again when asked to repeat it.

Return to Windows for one check:

**Terminal: Windows PowerShell · normal user.**

```powershell
wsl --list --verbose
```

**You should see:** Ubuntu 24.04 or 26.04 with `VERSION 2`. If the default install supplied a different release, run `wsl --list --online` and install a supported Ubuntu name from that list.

If the installed distribution is version 1, copy its exact name from the output above and replace `DISTRO-NAME` below:

**Terminal: Windows PowerShell · normal user.**

```powershell
wsl --set-version "DISTRO-NAME" 2
```

Now open **Ubuntu** from the Start menu. Every remaining block in this guide runs there unless it says otherwise. Confirm that this window is Linux:

**Terminal: Ubuntu in WSL · normal Linux user.**

```bash
printf 'shell=%s\n' "$SHELL"
uname -a
printf 'home=%s\n' "$HOME"
pwd
```

**You should see:** `/bin/bash`, a kernel string containing Microsoft or WSL, and a home path such as `/home/yourname`.

**Stop here if:** `/etc/os-release` is not Ubuntu 24.04 or 26.04, the distribution is still WSL 1, `$SHELL` does not end in `/bash`, you are logged in as `root`, or the home directory is under `/mnt/c`. This path writes Bash startup files, which are the small files Ubuntu reads each time you open a terminal.

Source: [Microsoft WSL environment setup](https://learn.microsoft.com/en-us/windows/wsl/setup/environment).

## 3. Install the base tools

Ubuntu installs software through `apt`, which downloads packages from Ubuntu's own servers. Its list of available packages must be refreshed before anything is installed. Node comes from `nvm` rather than `apt`, because Ubuntu's own Node package is often an older release than the course needs. Python 3.12 ships with Ubuntu 24.04 and is checked after the installation, not assumed.

**Terminal: Ubuntu in WSL · normal Linux user with `sudo` for apt only.** `sudo` runs one command with administrator rights and asks for the Linux password you created in step 2.

Expect this to take 5 to 20 minutes on a normal connection. It prints a long stream of download, unpack, and setup lines. Silence for a minute at a time is normal.

```bash
sudo apt update
sudo apt install -y git curl ca-certificates build-essential python3 python3-venv python3-pip xdg-utils
```

Next, install Node. The nvm installer is a script from the internet, so download it to a private temporary directory and read it before you run it.

**Terminal: Ubuntu in WSL · normal Linux user.**

```bash
tmp=$(mktemp -d)
curl -fsSL -o "$tmp/install-nvm.sh" https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.6/install.sh
```

The next two commands list the downloaded file and then open it in a pager, one screen at a time. Confirm the script belongs to the project it claims to come from: it should reference the `nvm-sh/nvm` repository, install into `$HOME/.nvm`, and append lines to your Bash startup file. If it fetches from some other repository, or asks for administrator rights, do not run it. Press **q** to leave the pager and return to the prompt.

```bash
ls -l "$tmp"
less "$tmp/install-nvm.sh"
```

Expect this to take 3 to 10 minutes. The installer prints a short summary, then `nvm install` prints download and checksum lines for the Node build.

```bash
bash "$tmp/install-nvm.sh"
rm -rf "$tmp"
export NVM_DIR="$HOME/.nvm"
. "$NVM_DIR/nvm.sh"
nvm install 24
nvm alias default 24
```

```bash
git --version
node --version
npm --version
python3 --version
```

**You should see:** a Git version, Node `v24.x`, an npm version, and Python `3.12` or later.

**Stop here if:** `apt update` reports repository or TLS errors, Node is not 24.x, Python is below 3.12, or the nvm installer does not name `nvm-sh/nvm`. Do not disable certificate checks. On an older Ubuntu release with Python below 3.12, run `wsl --list --online` in PowerShell and install Ubuntu 24.04 or 26.04 rather than adding an arbitrary PPA.

## 4. Put user tools on PATH

PATH is the list of folders your shell searches, in order, when you type a command name. A tool that is installed but not in one of those folders reports "command not found". Because Node came from `nvm`, npm already places global commands inside your Linux home directory. goose installs into `~/.local/bin`, so that one folder is added to PATH.

**Terminal: Ubuntu in WSL · normal Linux user.**

```bash
mkdir -p "$HOME/.local/bin"
case ":$PATH:" in
  *":$HOME/.local/bin:"*) ;;
  *) printf '\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$HOME/.bashrc" ;;
esac
export PATH="$HOME/.local/bin:$PATH"
npm config get prefix
printf '%s\n' "$PATH" | tr ':' '\n' | sed -n '1,8p'
```

**You should see:** an npm prefix such as `/home/yourname/.nvm/versions/node/v24.x.x`, and `/home/yourname/.local/bin` among the first lines of the PATH list.

**Stop here if:** npm's prefix is `/usr` or `/usr/local`, or you are about to use `sudo npm`. Close Ubuntu, open it again, and check that nvm loaded instead.

## 5. Clone and inspect the course

Cloning copies the course repository onto your machine. Keep it in the Linux filesystem: `/mnt/c` is the Windows drive seen from Linux, and it behaves differently for speed and file permissions.

**Terminal: Ubuntu in WSL · normal Linux user.**

```bash
mkdir -p "$HOME/course"
repo="$HOME/course/AI_Harness_Bootcamp"
if [ -e "$repo" ]; then
  printf 'STOP: %s already exists. Inspect it before reusing or renaming it.\n' "$repo" >&2
else
  git clone https://github.com/TheHolofex/AI_Harness_Bootcamp.git "$repo"
fi
cd "$repo"
git remote get-url origin
git rev-parse --short=12 HEAD
git status --short
pwd
```

**You should see:** the remote `https://github.com/TheHolofex/AI_Harness_Bootcamp.git`, a twelve-character revision, no lines from `git status`, and a path under `/home`, not `/mnt/c`.

**Stop here if:** the first line says `STOP:`, the remote differs, `git status` lists any path, or `pwd` starts with `/mnt/`.

## 6. Install the course applications

Install the Linux builds inside Ubuntu. If `command -v` later shows a path under `/mnt/c` or a Windows `.exe` or `.cmd`, the Windows copy is being used and the Linux one is missing.

**Terminal: Ubuntu in WSL · normal Linux user.**

Expect this to take 5 to 15 minutes on a normal connection. npm prints package counts and warning lines; warnings about optional dependencies do not stop the install.

```bash
npm install --global @openai/codex
npm install --global opencode-ai@1.18.17
npm install --global n8n@2.34.5
```

**You should see:** three `added … packages` summaries, one per command, and no error text. Lines beginning `npm warn` do not stop the install.

goose installs from a script, so download it to a private temporary directory first.

```bash
tmp=$(mktemp -d)
curl -fsSL -o "$tmp/goose-install.sh" https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh
```

The next two commands list the downloaded file and open it in the pager. Confirm the script matches this machine before you run it: it should reference the `aaif-goose/goose` repository, choose a Linux build, and choose the architecture your machine reported in the `uname -a` output in step 2 — `x86_64` or `aarch64`. If it names a different repository, or has no build for your architecture, do not run it. Press **q** to leave the pager.

```bash
ls -l "$tmp"
less "$tmp/goose-install.sh"
```

Expect this to take 1 to 3 minutes. It prints the release it selected and the path it installed to.

```bash
CONFIGURE=false bash "$tmp/goose-install.sh"
rm -rf "$tmp"
```

```bash
codex --version
opencode --version
goose --version
n8n --version
command -v codex opencode goose n8n
```

**You should see:** four Linux paths under your home directory, OpenCode `1.18.17`, and n8n `2.34.5`.

**Windows desktop, not a terminal.** Install Obsidian on Windows from [obsidian.md/download](https://obsidian.md/download). Open it, choose **Open folder as vault**, and enter the Linux repository through Explorer using this address:

```text
\\wsl$\Ubuntu\home\YOUR-LINUX-USER\course\AI_Harness_Bootcamp
```

Replace `YOUR-LINUX-USER` with the Linux username from step 2, and `Ubuntu` with the distribution name shown by `wsl --list --verbose` if it differs.

**Stop here if:** `command -v` resolves under `/mnt/c`, a Windows `.exe` is being used, goose has no build for this architecture, or Obsidian cannot open the address above. Do not create a second copy on the Windows drive; it will drift from the Ubuntu copy.

## 7. Connect the course accounts

Read [Connect the course accounts](../shared/CREDENTIALS.md), which sets the rules for handling the key.

**Terminal: Ubuntu in WSL · normal Linux user.**

```bash
codex login
codex login status
```

The key goes into this terminal process only. Run the next line **on its own**, with nothing else in the same paste. The command waits for input, and a shell that is still reading a pasted block will hand it the following line — capturing a command as your key without showing you.

```bash
IFS= read -r -s XAI_API_KEY
```

The cursor sits on a blank line with no prompt. Paste the key and press Enter. Nothing appears while you paste — no characters, no dots, no stars — and the prompt returns when you press Enter. Wait for that returned prompt before you paste anything else.

```bash
export XAI_API_KEY
export GOOSE_PROVIDER=xai
export GOOSE_MODEL=grok-4.5
if [ -n "${XAI_API_KEY:-}" ]; then printf 'SET\n'; else printf 'MISSING\n'; fi
```

**You should see:** the approved Codex login method, then `SET`. Never the key itself.

**Stop here if:** the check prints `MISSING`, Windows and WSL are signed into different Codex identities, the two lines above set anything other than `GOOSE_PROVIDER=xai` and `GOOSE_MODEL=grok-4.5`, or the key appears anywhere in terminal output or in a file.

## 8. Prove the setup

Check the local tools before making any request that costs money. Evidence is written to the Linux home directory, outside the clone, so the repository stays clean.

**Terminal: Ubuntu in WSL · normal Linux user.**

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
M0="reformation/AI_Harness_Bootcamp_2/module-00-setup"
export AHB_EVIDENCE_DIR="$HOME/course-evidence/module-00"
mkdir -p "$AHB_EVIDENCE_DIR"
bash "$M0/scripts/verify-setup.sh" "$PWD"
```

**You should see:** a `[PASS]` line for each check, `SETUP CHECK PASS` at the end, and a report path under `/home`.

**Stop here if:** the report ends with `SETUP CHECK HOLD`. Fix the first `[FAIL]` line, then run the same command again.

## 9. Repeat the proof in a fresh shell

Close the Ubuntu window and open a new one from the Start menu, and run every command below in that new window. A new window starts from your saved startup files alone, without anything the previous window set up by hand, so a tool that fails here has to be repaired here even though it answered a minute ago.

**Terminal: Ubuntu in WSL · normal Linux user · new window.**

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
command -v codex opencode goose n8n
node --version
if [ -n "${XAI_API_KEY:-}" ]; then printf 'SET — investigate persistence\n'; else printf 'MISSING — expected in a fresh shell\n'; fi
```

The key is session-only, so enter it again. Run the next line on its own, with nothing else in the same paste.

```bash
IFS= read -r -s XAI_API_KEY
```

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
M0="reformation/AI_Harness_Bootcamp_2/module-00-setup"
export XAI_API_KEY GOOSE_PROVIDER=xai GOOSE_MODEL=grok-4.5
export AHB_EVIDENCE_DIR="$HOME/course-evidence/module-00"
mkdir -p "$AHB_EVIDENCE_DIR"
run=$(mktemp -d "$AHB_EVIDENCE_DIR/run-XXXXXX")
printf '%s\n' "$run" > "$AHB_EVIDENCE_DIR/latest-run.txt"
mkdir "$run/proof"
bash "$M0/scripts/verify-setup.sh" "$PWD" "$run/setup-report.txt"
token=$(python3 -c 'import secrets; print(secrets.token_hex(4))')
printf '%s\n' "$token" > "$run/run-token.txt"
printf 'token=%s\n' "$token"
```

The token is a short random word created before the tools run. Each tool is asked to put it in the file it writes, and the check requires the file to carry this token and to have been written after the token file existed. That proves the file appeared during this run — not that a model rather than a person wrote it. Nothing running on your own machine can prove that.

```bash
run=$(cat "$HOME/course-evidence/module-00/latest-run.txt")
token=$(cat "$run/run-token.txt")
cd "$run/proof"
codex exec --sandbox workspace-write --skip-git-repo-check "Create a file named from-codex.txt whose only line is: codex works $token"
opencode run -m xai/grok-4.5 "Create a file named from-opencode.txt in the current directory whose only line is: opencode works $token"
goose run --no-session --provider xai --model grok-4.5 -t "Create a file named from-goose.txt in the current directory whose only line is: goose works $token"
```

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
M0="reformation/AI_Harness_Bootcamp_2/module-00-setup"
run=$(cat "$HOME/course-evidence/module-00/latest-run.txt")
python3 "$M0/shared/case/verify_tool_proof.py" "$run/proof" "$run/run-token.txt" | tee "$run/tool-proof.txt"
```

n8n holds the terminal it runs in, so start it in a second Ubuntu window. First start takes 1 to 3 minutes and prints database and migration lines, ending with an editor address on `localhost:5678`.

**Terminal: Ubuntu in WSL · normal Linux user · second window.**

```bash
n8n start
```

Back in the first window, ask n8n's own health endpoint whether it is n8n answering:

**Terminal: Ubuntu in WSL · normal Linux user · first window.**

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
M0="reformation/AI_Harness_Bootcamp_2/module-00-setup"
run=$(cat "$HOME/course-evidence/module-00/latest-run.txt")
python3 "$M0/shared/case/verify_n8n.py" "$run/n8n.pass"
```

Open `http://localhost:5678` in the Windows browser. The n8n editor page loads, which is Windows reaching a service running inside Ubuntu. Then switch to Obsidian on Windows and open the vault from step 6. Read two values from Obsidian itself: in its file list, the number of folders at the top level — the entries you can expand, before you expand any of them — and, in the vault switcher at the bottom left, the path it shows for this vault.

Type those two values into the first two lines below, in place of the words in capitals. Keep the single quotes around the path: a Windows path is full of backslashes, and without the quotes the shell removes them. The block counts the top-level folders in the clone itself and records both numbers, so the record holds what Obsidian showed you beside what is actually on disk. It keeps only the last two folder names of the path, so your user name stays out of the record.

**Terminal: Ubuntu in WSL · normal Linux user · first window.**

```bash
folders=REPLACE_WITH_THE_FOLDER_COUNT_OBSIDIAN_SHOWS
vault='REPLACE_WITH_THE_VAULT_PATH_OBSIDIAN_SHOWS'
cd "$HOME/course/AI_Harness_Bootcamp"
run=$(cat "$HOME/course-evidence/module-00/latest-run.txt")
clone_folders=$(ls -1d */ | wc -l | tr -d ' ')
vault_tail=$(printf '%s' "$vault" | tr '\\' '/' | awk -F/ '{print $(NF-1) "/" $NF}')
if ! printf '%s' "$folders" | grep -qE '^[0-9]+$'; then
  printf 'STOP: folders is still the placeholder. Type the number of top-level folders Obsidian lists.\n' >&2
elif ! printf '%s' "$vault" | grep -q 'AI_Harness_Bootcamp$'; then
  printf 'STOP: vault is still the placeholder. Copy the path from the vault switcher.\n' >&2
else
  printf 'obsidian-top-level-folders=%s\nclone-top-level-folders=%s\nobsidian-vault-ends-in=%s\n' \
    "$folders" "$clone_folders" "$vault_tail" > "$run/obsidian-observed.txt"
  test -d .obsidian && printf 'obsidian-config-written-here=yes\n' >> "$run/obsidian-observed.txt"
  cat "$run/obsidian-observed.txt"
fi
```

Then stop n8n in the second window with **Ctrl+C**.

**You should see:** `TOOL PROOF PASS`, `PASS: n8n answered its health check`, `obsidian-top-level-folders` and `clone-top-level-folders` carrying the same number, `obsidian-vault-ends-in=course/AI_Harness_Bootcamp`, and `obsidian-config-written-here=yes`. Every command ran in Ubuntu.

**Stop here if:** any command resolves to a Windows executable, the clone is under `/mnt`, a proof file is missing or carries the wrong token, a line begins `STOP:`, the two folder counts differ — which means Obsidian has a different folder open — `obsidian-config-written-here` is absent, or the key was written into `.bashrc`.

## 10. Save the setup record

The record holds what the checks observed, so it can be read later without rerunning anything. The folder count you read off Obsidian is compared against the clone before anything is written.

**Terminal: Ubuntu in WSL · normal Linux user.**

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
run=$(cat "$HOME/course-evidence/module-00/latest-run.txt")
report="$run/setup-report.txt"
observed=$(sed -n 's/^obsidian-top-level-folders=//p' "$run/obsidian-observed.txt" 2>/dev/null)
clone=$(ls -1d */ | wc -l | tr -d ' ')
missing=""
grep -q 'TOOL PROOF PASS' "$run/tool-proof.txt" 2>/dev/null || missing="$missing tool-proof"
test "$(cat "$run/n8n.pass" 2>/dev/null)" = PASS || missing="$missing n8n"
test -n "$observed" && [ "$observed" = "$clone" ] || missing="$missing obsidian-folder-count"
if [ -n "$missing" ]; then
  printf 'These records are missing or not passing:%s\n' "$missing" >&2
  printf 'Redo the matching part of step 9, then run this block again.\n' >&2
else
  case "$PWD" in
    /mnt/*) location="Windows filesystem" ;;
    *) location="Linux filesystem" ;;
  esac
  printf 'Setup path: Windows WSL 2 with Ubuntu\n' >> "$report"
  printf 'Repository location: %s\n' "$location" >> "$report"
  printf 'New-window file-writing checks: %s\n' "$(tail -n 1 "$run/tool-proof.txt")" >> "$report"
  printf 'n8n health check: %s\n' "$(cat "$run/n8n.pass")" >> "$report"
  cat "$run/obsidian-observed.txt" >> "$report"
  printf 'Target-platform execution: learner-run on this machine\n' >> "$report"
  tail -n 9 "$report"
fi
```

**You should see:** the last lines of the report reading `Repository location: Linux filesystem`, `New-window file-writing checks: TOOL PROOF PASS`, `n8n health check: PASS`, the two matching folder counts, and `obsidian-vault-ends-in=course/AI_Harness_Bootcamp` — and no key, user name, or hostname anywhere in them.

**Stop here if:** the block prints a missing record, or the report contains a Windows username, a key, an internal hostname, or an environment dump.

Continue to the [shared Module 0 lab](../shared/MODULE_00_LAB.md). Run it in Ubuntu, and use Windows Obsidian only to read and edit the same Linux files.
