# Arch Linux

This path assumes a supported Arch Linux installation with a desktop session. Arch updates continuously, so record the package versions installed today. The later checks show whether those versions work for the course. Reserve 75–150 minutes.

## 1. Before you change the machine

Read the machine's own values first, so that anything that changes later can be compared against a number you saw yourself.

**Terminal: Arch Linux terminal · normal user.**

```bash
cat /etc/arch-release
uname -m
df -h "$HOME"
printf 'desktop=%s\n' "${XDG_CURRENT_DESKTOP:-none}"
last_upgrade=$(grep '\[ALPM\] upgraded' /var/log/pacman.log 2>/dev/null | tail -n 1)
printf 'last_package_upgrade=%s\n' "${last_upgrade:-unknown}"
```

**You should see:** Arch Linux, `x86_64`, a desktop name such as `GNOME` or `KDE`, and the date of the most recent package upgrade. `df -h` prints a header row and one row of numbers for the filesystem holding your home directory; the free space is the figure under the `Avail` column, and it must be at least 15 GB. Official repository packages used here are currently published for x86_64. The last line is the newest `upgraded` entry in the pacman log; if its date is months old, expect the upgrade in step 3 to be at the long end of its range.

**Stop here if:** `Avail` is below 15 GB, architecture is unsupported by a required package, or no desktop is available for Obsidian. Do not try to solve architecture or desktop absence with an unreviewed AUR package.

## 2. Open the right terminal

Work as your normal user. `sudo` is used only for `pacman`.

**Terminal: Arch Linux terminal · normal user.**

```bash
id -un
printf 'shell=%s\n' "$SHELL"
printf 'home=%s\n' "$HOME"
```

**You should see:** your user and home, not `root`.

**Stop here if:** you are root or `$HOME` is not your user directory.

## 3. Install the base tools

Arch does not support partial upgrades. One `pacman -Syu` transaction refreshes the package databases and upgrades the system before any course package is installed.

Expect this to take 5 to 40 minutes, depending on how long it has been since the last upgrade. pacman lists the packages it will replace, then asks `:: Proceed with installation? [Y/n]` — press Return. After that it streams download and install lines. Silence for a minute at a time is normal.

**Terminal: Arch Linux terminal · normal user with `sudo` for pacman only.**

```bash
sudo pacman -Syu
```

If the upgraded list included `linux`, `glibc`, or `systemd`, restart the machine now and open a new terminal before you continue. Running the rest against a half-replaced kernel or C library produces errors that no later step can explain.

Expect the next command to take 3 to 15 minutes. It asks which members of the `base-devel` group to install — press Return to accept all of them — and then asks to proceed.

```bash
sudo pacman -S --needed git curl ca-certificates base-devel python npm nodejs-lts-krypton obsidian
```

```bash
git --version
node --version
npm --version
python --version
pacman -Q git nodejs-lts-krypton npm python obsidian
```

**You should see:** Node `v24.x`, Python `3.12+`, and one installed version line per package. On 2026-08-12, the official repository exposed Node 24 through `nodejs-lts-krypton`.

**Stop here if:** `pacman -Syu` fails, dependency conflicts remain, Node is not 24.x, Python is below 3.12, or a mirror error prevents a complete transaction. Do not run a database refresh without the full upgrade and do not continue from a partial transaction.

Sources: [Arch pacman](https://wiki.archlinux.org/title/Pacman), [Arch Node.js](https://wiki.archlinux.org/title/Node.js), and [Arch Python](https://wiki.archlinux.org/title/Python).

## 4. Put user tools on PATH

`PATH` is the list of folders your terminal searches, in order, when you type a command name. A command that is installed but not in one of those folders reports "command not found".

The course tools go in two folders you own, so that the commands live in your home directory instead of among the files `pacman` manages. Adding those folders to `PATH` in your shell's startup file is what makes the commands available in every terminal you open later.

**Terminal: Arch Linux terminal · normal user.**

```bash
mkdir -p "$HOME/.npm-global/bin" "$HOME/.local/bin"
npm config set prefix "$HOME/.npm-global"
case "$SHELL" in
  */zsh) profile="$HOME/.zshrc" ;;
  */bash) profile="$HOME/.bashrc" ;;
  *) profile="" ;;
esac
if [ -z "$profile" ]; then
  printf 'STOP: this path supports Bash or zsh. Observed login shell: %s\n' "$SHELL" >&2
else
  for line in 'export PATH="$HOME/.npm-global/bin:$PATH"' 'export PATH="$HOME/.local/bin:$PATH"'; do
    if ! grep -Fqx "$line" "$profile" 2>/dev/null; then
      if [ -s "$profile" ] && [ -n "$(tail -c 1 "$profile")" ]; then
        printf '\n' >> "$profile"
      fi
      printf '%s\n' "$line" >> "$profile"
    fi
  done
  printf 'profile=%s\n' "$profile"
fi
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"
prefix=$(npm config get prefix)
case "$prefix" in
  "$HOME"/*)
    if [ -w "$prefix" ]; then
      printf 'prefix=%s user-owned and writable\n' "$prefix"
    else
      printf 'STOP: prefix=%s exists but you cannot write to it\n' "$prefix" >&2
    fi ;;
  *) printf 'STOP: prefix=%s is outside your home directory\n' "$prefix" >&2 ;;
esac
```

Each line is added only if it is not already there, and only after a newline when the file does not already end in one, so nothing is joined onto whatever the last line was.

**You should see:** the path of the startup file that was updated, then `prefix=/home/<your user>/.npm-global user-owned and writable`.

**Stop here if:** any line begins with `STOP:`. npm pointing outside your home, or a prefix you cannot write to, will make every later install fail; do not work around it with `sudo npm install -g`.

## 5. Clone and inspect the course

Cloning makes your own copy of the course repository, with its history, in a folder you own. This step puts that copy under `~/course` and then reads three facts back off it: the address it came from, the revision you have, and whether anything in it has already been changed. If a folder already exists at the destination, nothing is written into it.

**Terminal: Arch Linux terminal · normal user.**

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
```

**You should see:** `https://github.com/TheHolofex/AI_Harness_Bootcamp.git`, a twelve-character revision, and no lines after it from `git status --short`.

**Stop here if:** the destination already existed, the remote is any other address, or `git status --short` prints a line. A clone that is already modified cannot serve as evidence later.

## 6. Install the course applications

Arch's official `opencode` package follows the newest release, so its version changes whenever you upgrade the system, and a result you get from it today may not be reproducible next week. Install the npm package at the version named below instead, so you can say afterwards exactly which version produced what you saw. No AUR helper is required.

Expect this to take 3 to 10 minutes on a normal connection. Each command prints a long stream of package lines and can sit silent for a minute at a time.

**Terminal: Arch Linux terminal · normal user.**

```bash
npm install --global @openai/codex
npm install --global opencode-ai@1.18.17
npm install --global n8n@2.34.5
```

goose is installed by a script published on its releases page. Download it into a private temporary folder first, and read it before it runs.

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
tmp=$(mktemp -d)
curl -fsSL --output-dir "$tmp" -O https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh
printf 'installer folder: %s\n' "$tmp"
ls -l "$tmp"
```

**You should see:** a folder path under `/tmp` ending in six random characters, and one file of a few kilobytes inside it.

Now read it. Confirm three things: it downloads from the `aaif-goose/goose` repository, it selects a Linux build, and it selects `x86_64`. Press `q` to leave the reader and return to the prompt.

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
less "$tmp/download_cli.sh"
```

**Stop here if:** the script fetches from any other repository, or names no build for your architecture. Do not run it to find out.

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
CONFIGURE=false bash "$tmp/download_cli.sh"
rm -r "$tmp"
```

```bash
codex --version
opencode --version
goose --version
n8n --version
```

**You should see:** OpenCode `1.18.17`, n8n `2.34.5`, and the Codex and goose versions installed today.

Open Obsidian and choose `~/course/AI_Harness_Bootcamp` as the vault.

**You should see:** the repository's folders in Obsidian's file explorer.

**Stop here if:** a pinned npm package fails against the current rolling system, goose publishes no binary for your architecture, Obsidian cannot open the folder, or `opencode` resolves to `/usr/bin/opencode` instead of your own copy. Check with `command -v opencode` and `pacman -Qo "$(command -v opencode)"` when the version is not the one you pinned.

## 7. Connect the course accounts

Read [Connect the course accounts](../shared/CREDENTIALS.md) before you start, then sign Codex in through its own browser flow.

**Terminal: Arch Linux terminal · normal user.**

```bash
codex login
codex login status
```

The cohort xAI key goes into this terminal process only. Run the next line **by itself** — paste nothing else with it. The terminal prints no prompt and shows no characters while you type or paste the key; that is what hiding the input looks like. Press Return when the key is in.

```bash
IFS= read -r -s XAI_API_KEY
```

```bash
export XAI_API_KEY
export GOOSE_PROVIDER=xai
export GOOSE_MODEL=grok-4.5
if [ -n "${XAI_API_KEY:-}" ]; then printf 'SET\n'; else printf 'MISSING\n'; fi
```

**You should see:** an approved authentication method from `codex login status`, then `SET` — and the key itself nowhere on screen.

**Stop here if:** any part of the key appears in the terminal, `MISSING` is printed, or the authentication method is not the one you were assigned.

## 8. Prove the setup

Check the local tools before making any request that may cost money. The report is written under `~/course-evidence/module-00`, outside the repository, so it cannot change the clone you just proved clean.

**Terminal: Arch Linux terminal · normal user · repository root.**

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
M0="reformation/AI_Harness_Bootcamp_2/module-00-setup"
export AHB_EVIDENCE_DIR="$HOME/course-evidence/module-00"
mkdir -p "$AHB_EVIDENCE_DIR"
bash "$M0/scripts/verify-setup.sh" "$PWD"
```

**You should see:** a `[PASS]` line for every check, then `SETUP CHECK PASS` and the path of the report.

**Stop here if:** the last line is `SETUP CHECK HOLD`. Fix the first `[FAIL]` line in the report before contacting an AI provider; the ones after it are often consequences of that one.

## 9. Repeat the proof in a fresh shell

Close this terminal and open a new one. Everything below runs in that new process, which is how you find out what your startup file actually loads.

**Terminal: Arch Linux terminal · normal user · new process.**

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
command -v node npm python3 codex opencode goose n8n
node --version
if [ -n "${XAI_API_KEY:-}" ]; then printf 'SET — investigate persistence\n'; else printf 'MISSING — expected in a fresh shell\n'; fi
```

**You should see:** seven absolute paths, `v24.x`, and `MISSING — expected in a fresh shell`. The key is session-only by design, so enter it again. Run the next line **by itself**; nothing is echoed while you paste.

```bash
IFS= read -r -s XAI_API_KEY
```

```bash
export XAI_API_KEY
export GOOSE_PROVIDER=xai
export GOOSE_MODEL=grok-4.5
cd "$HOME/course/AI_Harness_Bootcamp"
M0="reformation/AI_Harness_Bootcamp_2/module-00-setup"
export AHB_EVIDENCE_DIR="$HOME/course-evidence/module-00"
mkdir -p "$AHB_EVIDENCE_DIR"
run=$(mktemp -d "$AHB_EVIDENCE_DIR/run-XXXXXX")
printf '%s\n' "$run" > "$AHB_EVIDENCE_DIR/latest-run.txt"
proof="$run/proof"
mkdir "$proof"
token=$(python3 -c 'import secrets; print(secrets.token_hex(4))')
printf '%s\n' "$token" > "$run/run-token.txt"
bash "$M0/scripts/verify-setup.sh" "$PWD" "$run/setup-report.txt"
printf 'run=%s token=%s\n' "$run" "$token"
```

**You should see:** `SETUP CHECK PASS` again in this new terminal, then the folder holding this run's evidence and the eight-character token it just issued.

Each of the three tools is now asked to write one file containing that token. The token is what ties the file to this run: it did not exist until a moment ago, so a file carrying it was written after it was issued. It does not prove that a model rather than a person wrote the file — nothing running on your own machine can prove that.

```bash
cd "$proof"
codex exec --sandbox workspace-write --skip-git-repo-check "Create a file named from-codex.txt whose only line is: codex works $token"
opencode run -m xai/grok-4.5 "Create a file named from-opencode.txt in the current directory whose only line is: opencode works $token"
goose run --no-session --provider xai --model grok-4.5 -t "Create a file named from-goose.txt in the current directory whose only line is: goose works $token"
```

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
M0="reformation/AI_Harness_Bootcamp_2/module-00-setup"
python3 "$M0/shared/case/verify_tool_proof.py" "$proof" "$run/run-token.txt" | tee "$run/tool-proof.txt"
```

**You should see:** one `PASS:` line naming each of the three files, then `TOOL PROOF PASS`.

Start n8n in a second terminal with `n8n start` and leave it running. Back in this one:

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
M0="reformation/AI_Harness_Bootcamp_2/module-00-setup"
python3 "$M0/shared/case/verify_n8n.py" "$run/n8n.pass"
```

**You should see:** `PASS: n8n answered its health check at http://127.0.0.1:5678`. Stop n8n in the other terminal with **Ctrl+C** once you have that line.

Open the Obsidian vault again and read two values off the window: the vault's full path, shown when you click the vault name at the bottom left, and the number of files it reports in the status bar at the bottom right with no note open. If your version shows no count there, count the entries at the top level of the file explorer instead.

Type them in one at a time. Run the next line by itself, type the path Obsidian shows, and press Return.

```bash
IFS= read -r obsidian_path
```

Now the count, the same way.

```bash
IFS= read -r obsidian_count
```

The block below writes both values down beside a number the machine counts for itself, how many files Git tracks in the clone. It stops if the path you typed does not end in the course folder, or if the count you typed contains anything other than digits.

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
run=$(cat "$HOME/course-evidence/module-00/latest-run.txt")
tracked=$(git ls-files | wc -l)
path_ok=no
count_ok=no
case "$obsidian_path" in */course/AI_Harness_Bootcamp) path_ok=yes ;; esac
case "$obsidian_count" in ''|*[!0-9]*) count_ok=no ;; *) count_ok=yes ;; esac
if [ "$path_ok" = no ] || [ "$count_ok" = no ]; then
  printf 'STOP: path=%s count=%s. Type the two values Obsidian shows on screen, then run this block again.\n' "$obsidian_path" "$obsidian_count" >&2
else
  printf 'obsidian_vault_path=%s\nobsidian_file_count=%s\ngit_tracked_files=%s\n' \
    "$obsidian_path" "$obsidian_count" "$tracked" > "$run/obsidian.txt"
  cat "$run/obsidian.txt"
fi
```

**You should see:** three lines — the path you read off Obsidian, ending in `/course/AI_Harness_Bootcamp`; the count you read off Obsidian; and the number of files Git tracks. The two counts land in the same range but rarely match exactly, because Obsidian does not list files inside `.git` or other hidden folders. A count of `0`, or one several times the tracked number, means Obsidian has a different folder open.

**Stop here if:** a command disappeared in the new terminal, `TOOL PROOF HOLD` was printed, n8n did not answer, the block above printed `STOP:`, or `SET` came back before you entered the key. That last one means a key was written into a startup file, where every program that starts a shell can read it: have it revoked and replaced, then delete the line from your startup file.

## 10. Save the setup record

The checks you just ran each printed one line that matters. This step copies those lines into a single report under `~/course-evidence/module-00`, together with the version of every package the course depends on, so the state of this machine today is written down in one file you can read. Nothing is written into the clone.

**Terminal: Arch Linux terminal · normal user.**

```bash
cd "$HOME/course/AI_Harness_Bootcamp"
run=$(cat "$HOME/course-evidence/module-00/latest-run.txt")
report="$run/setup-report.txt"
{
  printf 'Setup path: Arch Linux\n'
  printf 'Tool proof: %s\n' "$(tail -n 1 "$run/tool-proof.txt" 2>/dev/null || printf 'not recorded')"
  printf 'n8n health check: %s\n' "$(cat "$run/n8n.pass" 2>/dev/null || printf 'not recorded')"
  cat "$run/obsidian.txt" 2>/dev/null || printf 'obsidian: not recorded\n'
  printf 'Target-platform execution: learner-run on this machine\n'
  pacman -Q git nodejs-lts-krypton npm python obsidian
} >> "$report"
tail -n 20 "$report"
```

**You should see:** `Tool proof: TOOL PROOF PASS`, `n8n health check: PASS`, the three Obsidian lines, and one version line per package — with no key, account identifier, or internal hostname anywhere in the output.

**Stop here if:** any line reads `not recorded`, or the report contains a secret, an account ID, an internal host, or a raw environment dump. Delete the report, have anything it exposed revoked, and rerun the step that wrote the offending line before the file leaves this machine.

Continue to the [shared Module 0 lab](../shared/MODULE_00_LAB.md).
