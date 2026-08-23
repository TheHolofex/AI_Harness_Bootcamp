# macOS

This path supports Apple Silicon and Intel Macs. Reserve 75–150 minutes. The commands are the same on both architectures. Homebrew installs into a different directory on each, so every step that needs that directory asks Homebrew where it is instead of hard-coding a path.

## 1. Before you change the machine

**Terminal: macOS Terminal · normal user.**

```bash
sw_vers
uname -m
df -h "$HOME"
xcode-select -p 2>/dev/null || true
```

**You should see:** a maintained macOS release, `arm64` or `x86_64`, and either a Command Line Tools path or no path yet. `df -h` prints a header row and one row of numbers; the free space is the figure under the `Avail` column, and it must be at least 15 GB.

**Stop here if:** `Avail` is below 15 GB, your organization blocks Terminal or software installation, or the architecture is neither `arm64` nor `x86_64`. Do not disable Gatekeeper or device management.

## 2. Open the right terminal

Open **Terminal** from Applications → Utilities. This guide uses the default zsh shell.

**Terminal: macOS Terminal · normal user.**

```zsh
printf 'shell=%s\n' "$SHELL"
printf 'zsh=%s\n' "${ZSH_VERSION:-missing}"
printf 'home=%s\n' "$HOME"
```

**You should see:** `/bin/zsh`, a zsh version rather than `missing`, and your home directory.

If Command Line Tools were missing in Step 1, start Apple's installer:

```bash
xcode-select --install
```

Complete the macOS dialog, then rerun `xcode-select -p`.

**Stop here if:** installation is blocked or `xcode-select -p` still fails after the dialog completes.

## 3. Install the base tools

Homebrew is a package manager for macOS: one command installs a tool along with everything it depends on. Its installer is a shell script, and a script is read before it is run.

**Terminal: macOS Terminal · normal user.**

Download the installer into a directory only you can read:

```bash
tmp=$(mktemp -d)
curl -fsSL -o "$tmp/install-homebrew.sh" https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh
ls -l "$tmp"
```

**You should see:** one file, a few tens of kilobytes, in a directory under `/var/folders` that only your account can read.

Read it before you run it. Three searches show where the file gets its code and where it puts it. `grep -n` prints every matching line with its line number.

```bash
cd "$tmp"
grep -n 'github.com/Homebrew/brew' install-homebrew.sh
grep -n '/opt/homebrew' install-homebrew.sh
grep -n '/usr/local' install-homebrew.sh
```

**You should see:** at least one numbered line from each search — a GitHub address ending in `Homebrew/brew`, the Apple Silicon directory `/opt/homebrew`, and the Intel directory `/usr/local`. If any search prints nothing, this file did not come from Homebrew: delete it and download it again from the address above.

Now page through the file to see what it does with those values. Press `q` to leave the pager.

```bash
cd "$tmp"
less install-homebrew.sh
```

Expect this to take 5 to 15 minutes on a normal connection. It prints a long stream of download lines and asks for your password once. Silence for a minute at a time is normal.

```bash
cd "$HOME"
if [ -f "$tmp/install-homebrew.sh" ]; then
  /bin/bash "$tmp/install-homebrew.sh"
  rm -rf "$tmp"
else
  printf 'STOP: the downloaded installer is not in this window. Run the download step again.\n' >&2
fi
```

At the end, Homebrew prints a `shellenv` command for this Mac. Run it now, and keep one copy of it in `~/.zprofile` so new Terminal windows find Homebrew too. The append starts with a blank line on purpose: when the last line of a file has no newline after it, appending joins two commands into one broken line, and the test that keeps a second copy out never matches again.

```zsh
if [ -x /opt/homebrew/bin/brew ]; then
  BREW_BIN=/opt/homebrew/bin/brew
elif [ -x /usr/local/bin/brew ]; then
  BREW_BIN=/usr/local/bin/brew
else
  BREW_BIN=""
fi
if [ -z "$BREW_BIN" ]; then
  printf 'STOP: no brew command in /opt/homebrew/bin or /usr/local/bin. Homebrew did not finish installing.\n' >&2
else
  eval "$($BREW_BIN shellenv)"
  brew_line='eval "$('"$BREW_BIN"' shellenv)"'
  grep -Fqx "$brew_line" "$HOME/.zprofile" 2>/dev/null || printf '\n%s\n' "$brew_line" >> "$HOME/.zprofile"
  printf 'brew=%s\n' "$(command -v brew)"
fi
```

**You should see:** `brew=/opt/homebrew/bin/brew` on Apple Silicon, or `brew=/usr/local/bin/brew` on Intel.

Now install the course runtimes. Expect this to take 10 to 40 minutes on a normal connection. Homebrew prints a long stream of download and build lines, and can sit silent for a minute at a time.

```bash
brew update
brew install git node@24 python@3.12
brew install --cask obsidian
```

**You should see:** from `brew update`, either `Already up-to-date.` or a list of the formulae it refreshed; then one summary line per package, each beginning with a beer glass and naming the directory it installed into, and `obsidian was successfully installed!` for the last command. No line begins with `Error:`.

Homebrew keeps Node 24 out of the way of any other Node on the machine, so its directory has to be added by name. Ask Homebrew for that directory rather than typing one:

```bash
node24_prefix="$(brew --prefix node@24 2>/dev/null)"
node24_bin="$node24_prefix/bin"
if [ -z "$node24_prefix" ] || [ ! -d "$node24_bin" ]; then
  printf 'STOP: Homebrew reports no directory for node@24. Install it before continuing.\n' >&2
else
  export PATH="$node24_bin:$PATH"
  printf 'node24_bin=%s\n' "$node24_bin"
fi
```

```bash
brew --version
git --version
node --version
npm --version
python3.12 --version
```

**You should see:** a `node24_bin` path ending in `/node@24/bin`, Node `v24.x`, and Python `3.12+`.

**Stop here if:** Homebrew is not under `/opt/homebrew` or `/usr/local`, a package build fails, Node is not 24.x, or Python is below 3.12. Keep the first Homebrew error; do not install a second package manager.

Sources: [Homebrew](https://brew.sh/), [Node.js](https://nodejs.org/en/download), and [Obsidian](https://obsidian.md/download).

## 4. Put user tools on PATH

`PATH` is the list of directories your shell searches, in order, when you type a command name. The first match wins, so a directory's position decides which `node` you get. This step puts the Node 24 directory, a user-owned npm directory, and goose's install directory at the front, and saves that order for future Terminal windows.

Nothing is written to your profile unless Homebrew reports a real Node 24 directory. An empty entry in `PATH` means "the directory I am standing in", which would make every future login shell search your working directory for commands.

**Terminal: macOS Terminal · normal user.**

```zsh
mkdir -p "$HOME/.npm-global/bin" "$HOME/.local/bin"
npm config set prefix "$HOME/.npm-global"
node24_prefix="$(brew --prefix node@24 2>/dev/null)"
node24_bin="$node24_prefix/bin"
if [ -z "$node24_prefix" ] || [ ! -d "$node24_bin" ]; then
  printf 'STOP: Homebrew reports no directory for node@24, so nothing was written to your profile.\n' >&2
else
  path_line='export PATH="'"$node24_bin"':$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"'
  grep -Fqx "$path_line" "$HOME/.zprofile" 2>/dev/null || printf '\n%s\n' "$path_line" >> "$HOME/.zprofile"
  export PATH="$node24_bin:$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"
  npm config get prefix
  command -v node npm python3.12
  node --version
  python3.12 --version
fi
```

**You should see:** a prefix under your home directory, `node` resolving inside Homebrew's `node@24` directory, Node `v24.x`, and Homebrew's Python 3.12. The order matters: it keeps an older `node` in `~/.local/bin` from being chosen instead of Node 24.

**Stop here if:** npm points to `/usr/local` or Homebrew's shared directories and asks for administrator ownership. Do not use `sudo npm install -g`.

## 5. Clone and inspect the course

Cloning makes your own copy of the course repository, with its history, in a folder you own. This step puts that copy under `~/course` and then reads three facts back off it: where it came from, which revision you have, and whether anything in it has already been changed. If a folder already exists at the destination, nothing is written into it — inspect it first, then rename or reuse it yourself.

**Terminal: macOS Terminal · normal user.**

Expect this to take 1 to 5 minutes. `git clone` prints counting and receiving lines, then stops.

```bash
mkdir -p "$HOME/course"
repo="$HOME/course/AI_Harness_Bootcamp"
if [ -e "$repo" ]; then
  printf 'STOP: %s already exists. Inspect it before reusing or renaming it.\n' "$repo" >&2
else
  git clone https://github.com/TheHolofex/AI_Harness_Bootcamp.git "$repo"
fi
if [ -d "$repo/.git" ]; then
  git -C "$repo" remote get-url origin
  git -C "$repo" rev-parse --short=12 HEAD
  git -C "$repo" status --short
fi
```

**You should see:** `https://github.com/TheHolofex/AI_Harness_Bootcamp.git`, a twelve-character revision, and no lines from `git status`.

**Stop here if:** the destination already existed, the remote is a different address, or `git status` prints any path. A dirty clone is checked later and will hold you there.

## 6. Install the course applications

**Terminal: macOS Terminal · normal user.**

Expect this to take 5 to 20 minutes on a normal connection. npm prints a long stream of progress lines and can sit silent for a minute at a time.

```zsh
npm install --global @openai/codex
npm install --global opencode-ai@1.18.17
npm install --global n8n@2.34.5
```

goose ships its own installer script. Download it into a directory only you can read:

```zsh
tmp=$(mktemp -d)
curl -fsSL -o "$tmp/goose-install.sh" https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh
ls -l "$tmp"
```

Read it before you run it. Confirm it downloads from the `aaif-goose/goose` releases on GitHub, that it selects the macOS build, and that it matches your architecture from Step 1 — `arm64` on Apple Silicon, `x86_64` on Intel. Press `q` to leave the pager.

```zsh
cd "$tmp"
less goose-install.sh
```

```zsh
cd "$HOME"
if [ -f "$tmp/goose-install.sh" ]; then
  CONFIGURE=false bash "$tmp/goose-install.sh"
  rm -rf "$tmp"
else
  printf 'STOP: the downloaded installer is not in this window. Run the download step again.\n' >&2
fi
```

```zsh
codex --version
opencode --version
goose --version
n8n --version
```

**You should see:** OpenCode `1.18.17`, n8n `2.34.5`, and a version string for Codex and for goose.

On first launch, macOS may block an application it has not seen before. Try opening it once. If you trust the official source and macOS still blocks it, open System Settings → Privacy & Security, find the blocked-app message, choose **Open Anyway**, authenticate, and confirm. Stop if the application name, source, or signature is not the one you downloaded. Do not disable Gatekeeper globally. See Apple's [Open a Mac app from an unidentified developer](https://support.apple.com/en-us/102445).

This path needs the Mac desktop. Run `launchctl print gui/$(id -u)`. If it fails, use a Mac where you can open Obsidian; a session over SSH alone cannot finish setup.

Open Obsidian from Applications. Choose **Open folder as vault** and select `~/course/AI_Harness_Bootcamp`.

**You should see:** the repository's folders in Obsidian's file list, and `AI_Harness_Bootcamp` as the vault name at the bottom left of the window.

**Stop here if:** macOS reports an unidentified or damaged binary from an unexpected source, an AI command resolves outside your home directory or Homebrew's directories, or a version differs from the two pinned above.

## 7. Connect the course accounts

Read [Connect the course accounts](../shared/CREDENTIALS.md).

**Terminal: macOS Terminal · normal user.**

```zsh
codex login
codex login status
```

The next command reads the cohort key without echoing it. Run that one line by itself, with nothing after it in the same paste: a shell reading hidden input takes the next pasted line as the answer, which would store a command as your key.

Copy the line, run it, paste the key at the blank cursor, and press Return.

```zsh
IFS= read -r -s XAI_API_KEY
```

Now hand the key to the tools that need it, for this window only:

```zsh
export XAI_API_KEY
export GOOSE_PROVIDER=xai
export GOOSE_MODEL=grok-4.5
key_len=${#XAI_API_KEY}
if [ "$key_len" -gt 0 ]; then printf 'XAI_API_KEY=SET, %s characters\n' "$key_len"; else printf 'XAI_API_KEY=MISSING\n'; fi
printf 'GOOSE_PROVIDER=%s GOOSE_MODEL=%s\n' "$GOOSE_PROVIDER" "$GOOSE_MODEL"
```

**You should see:** the account and method `codex login status` reports, `XAI_API_KEY=SET` with a character count, and `GOOSE_PROVIDER=xai GOOSE_MODEL=grok-4.5`. The key itself never appears.

**Stop here if:** the key value appears anywhere in the output, the character count is far shorter than the key you were issued, or the provider and model are not the two above.

## 8. Prove the setup

Check the local tools before making any request that may cost money. The report is saved outside the repository, which keeps course files separate from your setup results.

**Terminal: macOS Terminal · normal user · repository root.**

```zsh
cd "$HOME/course/AI_Harness_Bootcamp"
M0="reformation/AI_Harness_Bootcamp_2/module-00-setup"
export AHB_EVIDENCE_DIR="$HOME/course-evidence/module-00"
mkdir -p "$AHB_EVIDENCE_DIR"
bash "$M0/scripts/verify-setup.sh" "$PWD"
```

**You should see:** `SETUP CHECK PASS` and a report path under `~/course-evidence/module-00`.

**Stop here if:** the report ends with `SETUP CHECK HOLD`. Fix its first failed check before contacting an AI provider.

## 9. Repeat the proof in a fresh shell

Quit Terminal completely and reopen it. A new window loads your startup files and nothing else, so this is where you find out what you actually configured. You never wrote the key into a startup file, so you will type it in again by hand.

**Terminal: macOS Terminal · normal user · new process.**

```zsh
cd "$HOME/course/AI_Harness_Bootcamp"
command -v brew node npm python3.12 codex opencode goose n8n
node --version
if [ -n "${XAI_API_KEY:-}" ]; then printf 'key in this window: SET — investigate persistence\n'; else printf 'key in this window: MISSING — expected in a new window\n'; fi
```

**You should see:** eight command paths under your home directory or Homebrew's directories, Node `v24.x`, and `MISSING — expected in a new window`.

Enter the key again. This line runs by itself, for the same reason as in Step 7.

```zsh
IFS= read -r -s XAI_API_KEY
```

The block below creates this run's folder and a run token: a short random string, written to a file before any tool is asked to write anything. A proof file that carries this token was created during this run, after the token existed. It does not prove that a model rather than a person wrote it; nothing running on your own machine can prove that.

```zsh
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
printf 'run=%s\ntoken=%s\n' "$run" "$token"
```

**You should see:** `SETUP CHECK PASS` from the new window, a run folder under `~/course-evidence/module-00`, and an eight-character token.

Now ask each tool to write a file containing that token:

```zsh
cd "$HOME/course/AI_Harness_Bootcamp"
M0="$PWD/reformation/AI_Harness_Bootcamp_2/module-00-setup"
run=$(cat "$HOME/course-evidence/module-00/latest-run.txt")
token=$(cat "$run/run-token.txt")
proof="$run/proof"
cd "$proof"
codex exec --sandbox workspace-write --skip-git-repo-check "Create a file named from-codex.txt whose only line is: codex works $token"
opencode run -m xai/grok-4.5 "Create a file named from-opencode.txt in the current directory whose only line is: opencode works $token"
goose run --no-session --provider xai --model grok-4.5 -t "Create a file named from-goose.txt in the current directory whose only line is: goose works $token"
python3 "$M0/shared/case/verify_tool_proof.py" "$proof" "$run/run-token.txt" > "$run/tool-proof.txt" 2>&1
cat "$run/tool-proof.txt"
```

**You should see:** one `PASS:` line per file, then `TOOL PROOF PASS`. A `FAIL:` line names the file and what was wrong with it: missing, no token, the wrong token, or written before the token existed.

Start n8n in a second Terminal window with `n8n start`, and leave it running. Back in this window:

```zsh
cd "$HOME/course/AI_Harness_Bootcamp"
M0="$PWD/reformation/AI_Harness_Bootcamp_2/module-00-setup"
run=$(cat "$HOME/course-evidence/module-00/latest-run.txt")
python3 "$M0/shared/case/verify_n8n.py" "$run/n8n.pass" > "$run/n8n.txt" 2>&1
cat "$run/n8n.txt"
```

**You should see:** `PASS: n8n answered its health check at http://127.0.0.1:5678`.

Switch to Obsidian with the vault open. Its status bar, at the bottom of the window, reports how many files the vault contains. Read that number off the screen, then run the line below by itself, type the number, and press Return.

```zsh
IFS= read -r obsidian_files
```

The next block writes your number next to a number the machine counts for itself: how many files Git tracks in the clone. Obsidian and Git are looking at the same folder, so the two counts answer each other.

```zsh
cd "$HOME/course/AI_Harness_Bootcamp"
run=$(cat "$HOME/course-evidence/module-00/latest-run.txt")
tracked=$(git ls-files | wc -l | tr -d ' ')
case "$obsidian_files" in
  ''|*[!0-9]*)
    printf 'STOP: obsidian_files=%s is not a number. Rerun the read and type the count Obsidian shows.\n' "$obsidian_files" >&2 ;;
  *)
    printf 'obsidian-files-shown=%s\ngit-tracked-files=%s\n' "$obsidian_files" "$tracked" > "$run/obsidian-observed.txt"
    if [ -d .obsidian ]; then
      printf 'obsidian-vault-config=present in the folder you opened\n' >> "$run/obsidian-observed.txt"
    else
      printf 'obsidian-vault-config=absent — Obsidian has not opened this folder as a vault\n' >> "$run/obsidian-observed.txt"
    fi
    cat "$run/obsidian-observed.txt" ;;
esac
```

**You should see:** the count you read off Obsidian's status bar, the count Git tracks, and `obsidian-vault-config=present in the folder you opened`. The two counts are close but not equal, because Obsidian does not list the files inside `.git`. A count of `0`, or one many times larger than the tracked count, means Obsidian has a different folder open. Obsidian writes that configuration folder itself the first time it opens a vault, so its presence is the machine's own record of which folder the vault is.

Stop n8n in the other window with **Control+C**.

**Stop here if:** a command path from the earlier steps is missing, `TOOL PROOF PASS` does not appear, n8n does not answer, or `obsidian-vault-config` is absent. Stop as well if the new window reported `key in this window: SET`, or `grep -c XAI_API_KEY "$HOME/.zprofile"` returns anything above `0` — the key was written into a startup file, where every program that starts a shell can read it. Have that key revoked and replaced before you continue, then delete the line from `~/.zprofile`.

## 10. Save the setup record

Append the observed results to this run's report under `~/course-evidence/module-00`. Nothing is written into the clone.

**Terminal: macOS Terminal · normal user.**

```zsh
cd "$HOME/course/AI_Harness_Bootcamp"
run=$(cat "$HOME/course-evidence/module-00/latest-run.txt")
report="$run/setup-report.txt"
missing=""
for record in tool-proof.txt n8n.txt n8n.pass obsidian-observed.txt; do
  test -s "$run/$record" || missing="$missing $record"
done
if [ -n "$missing" ]; then
  printf 'STOP: this run has no record for:%s. Redo the step that produces it.\n' "$missing" >&2
else
  { printf 'Setup path: macOS\n'
    printf 'Tool proof: %s\n' "$(tail -n 1 "$run/tool-proof.txt")"
    printf 'n8n health check: %s\n' "$(tail -n 1 "$run/n8n.txt")"
    printf 'Obsidian: %s\n' "$(tr '\n' ' ' < "$run/obsidian-observed.txt")"
    printf 'Target-platform execution: learner-run on this machine\n'
  } >> "$report"
  tail -n 5 "$report"
fi
```

**You should see:** the five lines just appended, each carrying the line a check actually printed, with no key, account identifier, or home directory among them.

**Stop here if:** the appended lines include a key, an account ID, an internal hostname, or a dump of your environment. Delete the report, have anything it exposed revoked, and rerun the step that wrote the offending line before the file leaves this machine.

Continue to the [shared Module 0 lab](../shared/MODULE_00_LAB.md).
