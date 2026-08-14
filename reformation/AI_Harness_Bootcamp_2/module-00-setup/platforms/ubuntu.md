# Ubuntu

This path targets Ubuntu 24.04 LTS or 26.04 LTS with a desktop session. Reserve 75–150 minutes. Obsidian is required here, and it needs a graphical desktop, so a server install with no desktop cannot finish this setup. Use a machine with a desktop session.

## 1. Before you change the machine

Record what this machine is now, so that anything that fails later has a starting point you can compare against.

**Terminal: Ubuntu Terminal · normal user.**

```bash
. /etc/os-release
printf 'name=%s version=%s support=%s\n' "$PRETTY_NAME" "$VERSION_ID" "${UBUNTU_CODENAME:-unknown}"
uname -m
df -h "$HOME"
printf 'desktop=%s\n' "${XDG_CURRENT_DESKTOP:-none}"
```

**You should see:** `version=24.04` or `version=26.04`, and `x86_64` or `aarch64`. In the `df` table, the `Avail` column — the one between `Used` and `Use%` — reads `15G` or more; that column is the free space left, while `Size` is the whole disk. The last line reads `desktop=` followed by a name such as `ubuntu:GNOME`.

**Stop here if:** the release is not 24.04/26.04 LTS, `Avail` is below 15 GB, architecture has no required vendor binary, or `desktop=none`. A machine with no desktop session stops here, whatever the command-line checks report.

## 2. Open the right terminal

Every command in this guide runs in one place. Open Ubuntu's Terminal application and work as your normal user. Use `sudo` only where a step says so, which here means `apt` and the desktop package install.

**Terminal: Ubuntu Terminal · normal user.**

```bash
id -un
printf 'shell=%s\n' "$SHELL"
printf 'home=%s\n' "$HOME"
```

**You should see:** your user name, `/bin/bash`, and a home directory such as `/home/yourname`.

**Stop here if:** the user is `root`, `$HOME` is not your directory, or `$SHELL` does not end in `/bash`. This path writes Bash startup files.

## 3. Install the base tools

Git, Python and the build tools come from Ubuntu's own package archive. Node 24 comes from `nvm`, a small program that installs Node versions inside your home directory, so the Ubuntu release cannot quietly hand you an older Node.

Expect this to take 5 to 15 minutes on a normal connection. It prints a long stream of package names, download sizes and progress lines. A minute of silence while packages unpack is normal.

**Terminal: Ubuntu Terminal · normal user with `sudo` for apt only.**

```bash
sudo apt update
sudo apt install -y git curl ca-certificates build-essential python3 python3-venv python3-pip xdg-utils
```

Node's installer is a shell script from the `nvm` project. Download it to a private temporary directory first and read it before it runs.

```bash
nvm_tmp=$(mktemp -d)
curl -fsSL -o "$nvm_tmp/install-nvm.sh" https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.6/install.sh
ls -l "$nvm_tmp"
```

Confirm the file you just downloaded is the installer it claims to be. Read the next screen and check that it names the `nvm-sh/nvm` repository, writes into `$HOME/.nvm`, and appends to your Bash startup file. Nothing in it should fetch from a host you do not recognize. Press `q` to leave the pager.

```bash
# Press q to leave the pager and return to the prompt.
less "$nvm_tmp/install-nvm.sh"
```

Expect this to take 2 to 6 minutes. It prints download progress, then copies a Node build into your home directory. Silence for a minute at a time is normal.

```bash
bash "$nvm_tmp/install-nvm.sh"
rm -rf "$nvm_tmp"
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

**Stop here if:** `apt update` reports repository, proxy, or TLS errors; Python is below 3.12; or the installer text does not match what the paragraph above describes. Do not add an arbitrary PPA or disable TLS. If the installed Python is older than 3.12, move to Ubuntu 24.04 or 26.04 instead of adding an unofficial Python source.

Source: [Ubuntu package management](https://documentation.ubuntu.com/server/how-to/software/package-management/) and [Node.js](https://nodejs.org/en/download).

## 4. Put user tools on PATH

`PATH` is the list of folders your shell searches, in order, when you type a command name. A program that is installed but sits in a folder outside that list will report "command not found". Two folders need to be on it: the one `nvm` uses for Node's global commands, which it already added, and `~/.local/bin`, where goose puts its command.

**Terminal: Ubuntu Terminal · normal user.**

```bash
mkdir -p "$HOME/.local/bin"
case ":$PATH:" in
  *":$HOME/.local/bin:"*) ;;
  *) printf '\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$HOME/.bashrc" ;;
esac
export PATH="$HOME/.local/bin:$PATH"
prefix=$(npm config get prefix)
printf 'prefix=%s\n' "$prefix"
case "$prefix" in
  "$HOME"/*)
    if [ -w "$prefix" ]; then
      printf 'prefix is user-owned and writable\n'
    else
      printf 'prefix is inside your home but not writable\n'
    fi ;;
  *) printf 'prefix is outside your home: %s\n' "$prefix" ;;
esac
```

**You should see:** a prefix path under `/home/yourname/.nvm/versions/node/v24...`, and the line `prefix is user-owned and writable`.

**Stop here if:** the prefix is outside your home or not writable. Do not use `sudo npm install -g`; a global install owned by root leaves files your normal user cannot repair.

## 5. Clone and inspect the course

The course files live in your home directory, under `~/course`. An existing directory is never overwritten.

Expect this to take 1 to 5 minutes. Git prints object counts and a progress percentage.

**Terminal: Ubuntu Terminal · normal user.**

```bash
mkdir -p "$HOME/course"
repo="$HOME/course/AI_Harness_Bootcamp"
if [ -e "$repo" ]; then
  printf 'STOP: %s already exists. Inspect it before reusing or renaming it.\n' "$repo" >&2
else
  git clone https://github.com/TheHolofex/AI_Harness_Bootcamp.git "$repo"
fi
```

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
git remote get-url origin
git rev-parse --short=12 HEAD
git status --short
```

**You should see:** `https://github.com/TheHolofex/AI_Harness_Bootcamp.git`, a twelve-character revision, and no output at all from `git status --short`.

**Stop here if:** the destination already existed, the remote is a different address, or `git status --short` lists any path. A dirty clone is checked later, so repair it now.

## 6. Install the course applications

Codex, OpenCode and n8n come from npm; goose has its own installer. OpenCode and n8n are installed at an exact version rather than "latest", so a result you get on this machine can be reproduced on another one, and a change in behaviour has a smaller list of possible causes.

Expect this to take 5 to 20 minutes. npm prints a long stream of download and build lines, then a summary of added packages. Silence for a minute at a time is normal.

**Terminal: Ubuntu Terminal · normal user.**

```bash
npm install --global @openai/codex
npm install --global opencode-ai@1.18.17
npm install --global n8n@2.34.5
```

**You should see:** three `added … packages` summaries, one per command, and no error text. Lines beginning `npm warn` do not stop the install.

goose is installed by a shell script from its official release page. Download it to a private temporary directory first and read it before it runs.

```bash
goose_tmp=$(mktemp -d)
curl -fsSL -o "$goose_tmp/goose-install.sh" https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh
ls -l "$goose_tmp"
```

Confirm the file you just downloaded is goose's own installer. Read the next screen and check that it names the `aaif-goose/goose` repository, that it selects a Linux build matching the architecture you saw in step 1 (`x86_64` or `aarch64`), and that it installs into `$HOME/.local/bin`. Press `q` to leave the pager.

```bash
# Press q to leave the pager and return to the prompt.
less "$goose_tmp/goose-install.sh"
```

```bash
CONFIGURE=false bash "$goose_tmp/goose-install.sh"
rm -rf "$goose_tmp"
```

```bash
codex --version
opencode --version
goose --version
n8n --version
```

**You should see:** OpenCode `1.18.17`, n8n `2.34.5`, and a version number for Codex and for goose.

Now install Obsidian. Open [Obsidian's official download page](https://obsidian.md/download) in a browser and download the current Linux build for your architecture: on `x86_64` the `.deb` package, on `aarch64` the ARM64 `.tar.gz` archive. Use only that page.

**Terminal: Ubuntu Terminal · normal user; `sudo` only for the amd64 package install.**

On `x86_64`, install the downloaded package. Expect this to take 1 to 3 minutes; `apt` prints the package name, its size, and an unpacking line.

```bash
obsidian_deb=$(ls -1t "$HOME"/Downloads/obsidian_*_amd64.deb 2>/dev/null | head -n 1)
if [ -z "$obsidian_deb" ]; then
  printf 'STOP: no obsidian_*_amd64.deb found in %s/Downloads\n' "$HOME" >&2
else
  printf 'installing=%s\n' "$obsidian_deb"
  sudo apt install "$obsidian_deb"
fi
```

On `aarch64`, unpack the archive into your own home directory instead. Do not use the ARM64 AppImage: it loads `libfuse.so.2`, which Ubuntu 24.04 does not install by default, so it stops with `dlopen(): error loading libfuse.so.2`. The archive needs nothing extra.

```bash
obsidian_tar=$(ls -1t "$HOME"/Downloads/obsidian-*-arm64.tar.gz 2>/dev/null | head -n 1)
if [ -z "$obsidian_tar" ]; then
  printf 'STOP: no obsidian-*-arm64.tar.gz found in %s/Downloads\n' "$HOME" >&2
else
  printf 'unpacking=%s\n' "$obsidian_tar"
  mkdir -p "$HOME/.local/opt/obsidian"
  tar -xzf "$obsidian_tar" -C "$HOME/.local/opt/obsidian" --strip-components=1
  ls -1 "$HOME/.local/opt/obsidian" | head -n 5
fi
```

On `x86_64`, start Obsidian from the applications menu. On `aarch64`, start it with the command below. Obsidian holds the terminal while it runs, and the prompt returns only when you close the window, so open a second terminal window if you need one meanwhile.

```bash
obsidian_bin=$(ls -1 "$HOME/.local/opt/obsidian"/[Oo]bsidian 2>/dev/null | head -n 1)
if [ -z "$obsidian_bin" ]; then
  printf 'STOP: no Obsidian program in %s/.local/opt/obsidian\n' "$HOME" >&2
else
  printf 'launching=%s\n' "$obsidian_bin"
  "$obsidian_bin"
fi
```

In Obsidian choose **Open folder as vault** and select `~/course/AI_Harness_Bootcamp`.

**You should see:** on `aarch64`, a `launching=` line naming the Obsidian program; and on either architecture, once the vault opens, the course files in Obsidian's left-hand file list, including `README.md`.

**Stop here if:** the downloaded file's architecture does not match the `uname -m` value from step 1, the file came from a mirror rather than obsidian.md, Obsidian will not open, or a pinned version differs from `1.18.17` for OpenCode or `2.34.5` for n8n.

## 7. Connect the course accounts

Read [Connect the course accounts](../shared/CREDENTIALS.md) before you start. Codex signs in through its own browser flow. The xAI key is loaded into this terminal process only, and never written to a file.

**Terminal: Ubuntu Terminal · normal user.**

```bash
codex login
codex login status
```

Now load the cohort key. Run the single line below on its own, with nothing after it in the same paste: the shell feeds whatever follows a hidden-input command straight into it, so a pasted second line would be captured as your key. Nothing appears on screen while you paste the key. Press Enter when you have pasted it.

```bash
IFS= read -r -s XAI_API_KEY
```

```bash
export XAI_API_KEY
export GOOSE_PROVIDER=xai
export GOOSE_MODEL=grok-4.5
if [ -n "${XAI_API_KEY:-}" ]; then printf 'SET\n'; else printf 'MISSING\n'; fi
```

**You should see:** the authentication method Codex reports, and the single word `SET`. The key itself is never printed.

**Stop here if:** any part of the key appears on screen, `MISSING` is printed, or the two lines above set anything other than `GOOSE_PROVIDER=xai` and `GOOSE_MODEL=grok-4.5`.

## 8. Prove the setup

Check the local tools before making any request that may cost money. Evidence is written to `~/course-evidence/module-00`, outside the clone, so that checking your work cannot change the files being checked.

**Terminal: Ubuntu terminal · normal user · repository root.**

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
M0="reformation/AI_Harness_Bootcamp_2/module-00-setup"
export AHB_EVIDENCE_DIR="$HOME/course-evidence/module-00"
mkdir -p "$AHB_EVIDENCE_DIR"
bash "$M0/scripts/verify-setup.sh" "$PWD"
```

**You should see:** a `[PASS]` line for each check, ending with `SETUP CHECK PASS`, and the path of a report file under `~/course-evidence/module-00`.

**Stop here if:** the report ends with `SETUP CHECK HOLD`. Work on the first `[FAIL]` line only, then run the check again, before contacting an AI provider.

## 9. Repeat the proof in a fresh shell

Close this terminal and open a new one, and run everything below in that new terminal. A new terminal starts from your saved startup files alone, without anything the previous session set up by hand, so a tool that fails here has to be repaired here even though it answered a minute ago.

**Terminal: Ubuntu terminal · normal user · new process.**

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
command -v node npm python3 codex opencode goose n8n
node --version
if [ -n "${XAI_API_KEY:-}" ]; then printf 'SET — investigate persistence\n'; else printf 'MISSING — expected in a fresh shell\n'; fi
```

The key is deliberately gone. Load it again, running this single line on its own as before.

```bash
IFS= read -r -s XAI_API_KEY
```

Now create this run's evidence directory and its token. The token is a short random string, written to a file before the AI tools run. A proof file that carries it must have been written after the token existed, which is to say during this run. It does not show that a model rather than a person typed the file; nothing running on your own machine can show that.

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
M0="reformation/AI_Harness_Bootcamp_2/module-00-setup"
export XAI_API_KEY GOOSE_PROVIDER=xai GOOSE_MODEL=grok-4.5
export AHB_EVIDENCE_DIR="$HOME/course-evidence/module-00"
mkdir -p "$AHB_EVIDENCE_DIR"
run=$(mktemp -d "$AHB_EVIDENCE_DIR/run-XXXXXX")
printf '%s\n' "$run" > "$AHB_EVIDENCE_DIR/latest-run.txt"
mkdir "$run/proof"
token=$(python3 -c 'import secrets; print(secrets.token_hex(4))')
printf '%s\n' "$token" > "$run/run-token.txt"
printf 'run=%s token=%s\n' "$run" "$token"
bash "$M0/scripts/verify-setup.sh" "$PWD" "$run/setup-report.txt"
```

Ask each tool to write one file. Each prompt carries this run's token, so the file each tool leaves behind can be tied to this run.

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

n8n runs in the foreground and holds its terminal. Open a second terminal window and start it there.

**Terminal: a second Ubuntu terminal · normal user.**

```bash
n8n start
```

Back in the first terminal, ask n8n's own health endpoint whether it is n8n answering, rather than trusting an open port.

**Terminal: Ubuntu terminal · normal user · new process.**

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
M0="reformation/AI_Harness_Bootcamp_2/module-00-setup"
run=$(cat "$HOME/course-evidence/module-00/latest-run.txt")
python3 "$M0/shared/case/verify_n8n.py" "$run/n8n.pass"
```

Leave n8n running for now. Switch to Obsidian with the course vault open. In its file list, count the folders at the top level — the entries you can expand, before you expand any of them. Then open the vault switcher at the bottom left and read the path it shows for this vault. Type those two values into the first two lines below, in place of the words in capitals, keeping the single quotes around the path. The block counts the top-level folders in the clone itself and records both numbers, so the record holds what Obsidian showed you beside what is actually on disk. It keeps only the last two folder names of the path, so your home directory and user name stay out of the record.

```bash
folders=REPLACE_WITH_THE_FOLDER_COUNT_OBSIDIAN_SHOWS
vault='REPLACE_WITH_THE_VAULT_PATH_OBSIDIAN_SHOWS'
cd "$HOME/course/AI_Harness_Bootcamp"
run=$(cat "$HOME/course-evidence/module-00/latest-run.txt")
clone_folders=$(ls -1d */ | wc -l | tr -d ' ')
vault_tail=$(printf '%s' "$vault" | awk -F/ '{print $(NF-1) "/" $NF}')
if ! printf '%s' "$folders" | grep -qE '^[0-9]+$'; then
  printf 'STOP: folders is still the placeholder. Type the number of top-level folders Obsidian lists.\n' >&2
elif ! printf '%s' "$vault" | grep -q 'AI_Harness_Bootcamp$'; then
  printf 'STOP: vault is still the placeholder. Copy the path from the vault switcher.\n' >&2
else
  printf 'obsidian-top-level-folders=%s\nclone-top-level-folders=%s\nobsidian-vault-ends-in=%s\n' \
    "$folders" "$clone_folders" "$vault_tail" > "$run/obsidian-observed.txt"
  cat "$run/obsidian-observed.txt"
fi
```

Stop n8n in the second terminal with **Ctrl+C** once the n8n check has printed its result.

**You should see:** an absolute path for each of the seven commands, Node `v24.x`, `MISSING — expected in a fresh shell`, `SETUP CHECK PASS`, three `PASS:` lines ending in `TOOL PROOF PASS`, `PASS: n8n answered its health check at http://127.0.0.1:5678`, and three `obsidian-` lines in which `obsidian-top-level-folders` and `clone-top-level-folders` carry the same number and `obsidian-vault-ends-in` reads `course/AI_Harness_Bootcamp`.

**Stop here if:** `command -v` prints nothing for a tool, the fresh shell reports `SET`, a proof line reads `FAIL:` or `HOLD:`, a line begins `STOP:`, or the two folder counts differ — a different count means Obsidian has a different folder open.

## 10. Save the setup record

The record is assembled from the values the checks produced, and the folder count you read off Obsidian is compared against the clone itself.

**Terminal: Ubuntu terminal · normal user.**

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
run=$(cat "$HOME/course-evidence/module-00/latest-run.txt")
expected=$(ls -1d */ | wc -l | tr -d ' ')
observed=$(sed -n 's/^obsidian-top-level-folders=//p' "$run/obsidian-observed.txt" 2>/dev/null)
vault=$(sed -n 's/^obsidian-vault-ends-in=//p' "$run/obsidian-observed.txt" 2>/dev/null)
case "$vault" in course/AI_Harness_Bootcamp) vault_ok=yes ;; *) vault_ok=no ;; esac
if grep -q 'TOOL PROOF PASS' "$run/tool-proof.txt" 2>/dev/null; then tool=PASS; else tool=HOLD; fi
n8n=$(cat "$run/n8n.pass" 2>/dev/null || printf 'HOLD')
printf 'tool-proof=%s n8n=%s obsidian-folders=%s clone-folders=%s vault-is-the-clone=%s\n' \
  "$tool" "$n8n" "${observed:-none}" "$expected" "$vault_ok"
```

```bash
run=$(cat "$HOME/course-evidence/module-00/latest-run.txt")
report="$run/setup-report.txt"
if [ "$tool" = PASS ] && [ "$n8n" = PASS ] && [ "$observed" = "$expected" ] && [ "$vault_ok" = yes ]; then
  cat >> "$report" <<EOF
Setup path: Ubuntu
Fresh-terminal file-writing checks: TOOL PROOF PASS
n8n health endpoint: PASS
Obsidian vault top-level folders: $observed, matching the $expected in the clone
Obsidian vault path ends in: $vault
Target-platform execution: learner-run on this machine
EOF
  printf 'record appended: %s\n' "$report"
else
  printf 'Not ready to submit: tool-proof=%s n8n=%s obsidian-folders=%s clone-folders=%s vault-is-the-clone=%s\n' \
    "$tool" "$n8n" "${observed:-none}" "$expected" "$vault_ok" >&2
fi
```

**You should see:** one line reading `tool-proof=PASS n8n=PASS`, the same number in `obsidian-folders` and `clone-folders`, and `vault-is-the-clone=yes`; then `record appended:` and the path of the report.

**Stop here if:** the line begins `Not ready to submit`, the two folder counts differ, or the report contains a key, an account identifier, an internal host name, or a raw environment dump.

Continue to the [shared Module 0 lab](../shared/MODULE_00_LAB.md).
