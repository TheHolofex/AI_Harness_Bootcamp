# Ubuntu setup for Module 0

This takes an ordinary Ubuntu desktop account through a checked Oh My Pi install, a course checkout, and one live proof file. Plan for 45 to 90 minutes. A package install can take longer on a slow connection. Wait for the prompt to return before you paste the next box.

You need Git, Python 3.12 or newer, a web browser, an ordinary text editor, and Oh My Pi 18.3.5. The live proof uses one OpenRouter key and the model `openrouter/anthropic/claude-sonnet-4.6`. This path does not install Node, npm, or a second AI tool, and it does not ask you to log in to a model vendor.

Every command box is one paste. Select every line in the box, paste it once, and press Return. The commands use absolute paths, so your current folder does not matter. A home folder with spaces is fine, because every path is quoted.

The steps are: check the machine, install any missing Ubuntu packages, choose Python, download and verify Oh My Pi, install it without replacing a different copy, record the user folder on PATH, use the course checkout, prove a newly opened terminal, enter the key, run one proof, and save a prerequisite report.

Keep these pages open beside this one: [versions](../shared/VERSIONS.md), [credentials](../shared/CREDENTIALS.md), [sources](../shared/SOURCES.md), and [when setup stops](../shared/TROUBLESHOOTING.md).

## 1. Check the machine

You need a supported processor family and enough free space in your home folder before any download.

**Terminal: Ubuntu, ordinary user.**

```bash
uname -m
df -h "$HOME"
```

**Expected:** The first line is `x86_64`, `aarch64`, or `arm64`. In the disk table, the Available column for your home filesystem is at least 15G.

**Stop:** The processor family is anything else, or Available is below 15G.

**Recovery:** This path has no other Linux build. Free space in your home folder until Available is at least 15G, then run the two commands again. Do not download a binary for a different processor.

## 2. See whether the Ubuntu packages are already installed

Git, curl, and Python come from Ubuntu's own packages. This check only looks. It does not install or remove anything.

**Terminal: Ubuntu, ordinary user.**

```bash
course_check_packages() {
  local missing=""
  command -v git >/dev/null 2>&1 || missing="git"
  command -v curl >/dev/null 2>&1 || missing="${missing:+$missing }curl"
  command -v python3 >/dev/null 2>&1 || missing="${missing:+$missing }python3"
  if [ -z "$missing" ]; then
    printf 'PACKAGES present\n'
  else
    printf 'PACKAGES missing: %s\n' "$missing"
  fi
}
course_check_packages
```

**Expected:** The line is `PACKAGES present`, or it names one or more of `git`, `curl`, and `python3`.

**Stop:** The command prints an error instead of one of those lines, or you are not in the Ubuntu Terminal application.

**Recovery:** Open the Ubuntu Terminal application as your ordinary user and paste the box again. If the line names missing packages, continue to the next step. If it says `PACKAGES present`, skip the install step and continue at the Python step. An older `python3` can still be present; the Python step is what rejects a version below 3.12.

## 3. Install missing Ubuntu packages

This is the only step that asks for an administrator password. Ubuntu 24.04's `python3` package is Python 3.12, and Ubuntu 26.04's `python3` package is Python 3.14. Both meet the course floor. The install uses that distro package, plus Git, curl, and the certificate bundle. Package names and the `apt-get` command are Ubuntu's, as described in [Ubuntu package management](https://documentation.ubuntu.com/server/how-to/software/package-management/).

Skip this box when the previous step printed `PACKAGES present`.

**Terminal: Ubuntu, elevated package installation.**

```bash
sudo apt-get update && sudo apt-get install -y git python3 ca-certificates curl
```

**Expected:** `apt-get` finishes and returns you to the prompt. It may ask for your password before it installs. Already-installed packages stay in place.

**Stop:** `sudo` is missing, the password is rejected, a device policy refuses the install, or `apt-get` stops with an error. A failed update must not be followed by a separate install command.

**Recovery:** Stop. Do not add a personal package archive, download Python from the web, or use pip to get around the refusal. Save the exact error and use [when setup stops](../shared/TROUBLESHOOTING.md). When the device owner has approved the packages, paste this box again.

## 4. Choose the Python interpreter

The later checks must call one real Python executable, not a name that might point somewhere else. This step uses the first of python3.12, python3, or python that reports >= 3.12 via sys.executable and keeps the absolute path.

**Terminal: Ubuntu, ordinary user.**

```bash
course_resolve_python() {
  PY="$(for candidate in python3.12 python3 python; do "$candidate" -c 'import sys; sys.exit(1) if sys.version_info < (3, 12) else print(sys.executable)' 2>/dev/null && break; done)"
  if [ -n "$PY" ]; then
    printf 'PY %s\n' "$PY"
    "$PY" --version
    return 0
  fi
  printf 'STOP: no real Python executable is version 3.12 or newer\n' >&2
  return 1
}
course_resolve_python
```

**Expected:** A line starting with `PY ` gives an absolute path, and the next line starts with `Python 3.12` or newer.

**Stop:** You see the STOP line, no `PY` line, or a version below 3.12.

**Recovery:** If the package step was skipped and the interpreter is too old, return to the elevated install and run it. If Ubuntu's python3 package is already installed and is still older than 3.12, stop. Do not add another Python repository. Save the version line and ask the device owner.
## 5. Download Oh My Pi into a fresh folder

You are downloading the pinned release file and its official checksum list. Nothing is made executable in this step, and nothing is copied into the command folder. The checksum file also lists musl builds. This path selects only `omp-linux-arm64` for `aarch64` or `arm64`, or `omp-linux-x64` for `x86_64`. The files come from the [v18.3.5 release](https://github.com/can1357/oh-my-pi/releases/tag/v18.3.5). This path does not use the project's installer script.

Each attempt has its own folder under your home directory. A failed download stays there. The next try creates a new folder instead of reusing it.

**Terminal: Ubuntu, ordinary user.**

```bash
course_download_omp() {
  local arch asset attempt download
  unset OMP_ASSET OMP_DOWNLOAD_DIR
  arch="$(uname -m)" || return 1
  case "$arch" in
    aarch64|arm64) asset="omp-linux-arm64" ;;
    x86_64) asset="omp-linux-x64" ;;
    *)
      printf 'STOP: unsupported architecture %s\n' "$arch" >&2
      return 1
      ;;
  esac
  attempt="omp-download-$(date -u +%Y%m%dT%H%M%SZ)-$$"
  download="$HOME/course-evidence/reformation-qa/$attempt"
  if [ -e "$download" ] || [ -L "$download" ]; then
    printf 'STOP: %s already exists and was not reused\n' "$download" >&2
    return 1
  fi
  mkdir -p -- "$download" || return 1
  if ! curl -fL --output "$download/$asset" "https://github.com/can1357/oh-my-pi/releases/download/v18.3.5/$asset"; then
    printf 'STOP: binary download failed; nothing was installed or executed\n' >&2
    return 1
  fi
  if ! curl -fL --output "$download/SHA256SUMS.txt" "https://github.com/can1357/oh-my-pi/releases/download/v18.3.5/SHA256SUMS.txt"; then
    printf 'STOP: checksum download failed; nothing was installed or executed\n' >&2
    return 1
  fi
  OMP_ASSET="$asset"
  OMP_DOWNLOAD_DIR="$download"
  printf 'DOWNLOADED %s\n' "$download/$asset"
}
course_download_omp
```

**Expected:** One line starts with `DOWNLOADED ` and names a new folder under your home directory, ending in `omp-linux-arm64` or `omp-linux-x64`.

**Stop:** You see a STOP line, curl reports an error, or the line names a musl file. Do not continue to the install step after a STOP line.

**Recovery:** Leave the failed folder in place. Do not delete it to retry, and do not disable certificate checks. If the error mentions a certificate or a proxy, run the elevated package step so `ca-certificates` is installed, then paste this box again. The new paste creates a new folder. Use [when setup stops](../shared/TROUBLESHOOTING.md) if the same certificate error returns.

## 6. Verify the checksum and install the binary

A checksum is a fingerprint for a file. Here it is a 64-character hexadecimal value from `SHA256SUMS.txt`. The install runs only after exactly one well-formed line names the selected file and the downloaded bytes match that value. A missing line, a second line, or a mismatch stops the function before the file is made executable, copied, or run.

The destination is `"$HOME/.local/bin/omp"`. An existing different file is left untouched. A shortcut at that path is left untouched. A file that already matches the verified download is kept.

**Terminal: Ubuntu, ordinary user.**

```bash
course_install_omp() {
  local asset download sums expected actual dest version
  asset="${OMP_ASSET:-}"
  download="${OMP_DOWNLOAD_DIR:-}"
  case "$asset" in
    omp-linux-arm64|omp-linux-x64) ;;
    *)
      printf 'STOP: no selected Linux asset is recorded in this terminal\n' >&2
      return 1
      ;;
  esac
  if [ -z "$download" ] || [ ! -d "$download" ] || [ -L "$download" ]; then
    printf 'STOP: no fresh download directory is recorded in this terminal\n' >&2
    return 1
  fi
  sums="$download/SHA256SUMS.txt"
  if ! expected="$(awk -v asset="$asset" '
    BEGIN { count = 0; hash = "" }
    {
      gsub(/\r/, "")
      if ($2 == asset && NF == 2) { count++; hash = $1 }
    }
    END {
      if (count != 1) exit 2
      if (hash !~ /^[0-9a-fA-F]{64}$/) exit 3
      print hash
    }
  ' "$sums")"; then
    printf 'STOP: checksum entry for %s is absent, ambiguous, or not a 64-character hex digest\n' "$asset" >&2
    return 1
  fi
  if [ ! -f "$download/$asset" ] || [ -L "$download/$asset" ]; then
    printf 'STOP: downloaded file is missing or is a symlink\n' >&2
    return 1
  fi
  actual="$(sha256sum -- "$download/$asset" | awk '{ print $1 }')" || return 1
  if [ "$actual" != "$expected" ]; then
    printf 'STOP: checksum mismatch; the binary was not installed or executed\n' >&2
    return 1
  fi
  chmod +x -- "$download/$asset" || return 1
  if [ -L "$HOME/.local/bin" ]; then
    printf 'STOP: %s is a symlink; the binary was not installed there\n' "$HOME/.local/bin" >&2
    return 1
  fi
  mkdir -p -- "$HOME/.local/bin" || return 1
  dest="$HOME/.local/bin/omp"
  if [ -L "$dest" ]; then
    printf 'STOP: %s is a symlink; it was not replaced\n' "$dest" >&2
    return 1
  fi
  if [ -e "$dest" ]; then
    if [ ! -f "$dest" ] || ! cmp -s -- "$download/$asset" "$dest"; then
      printf 'STOP: destination exists and differs; it was not overwritten\n' >&2
      return 1
    fi
    printf 'KEEP: destination already matches the verified download\n'
  else
    cp -- "$download/$asset" "$dest" || return 1
    if [ -L "$dest" ] || ! cmp -s -- "$download/$asset" "$dest"; then
      printf 'STOP: copy does not match the verified download\n' >&2
      return 1
    fi
    printf 'INSTALLED %s\n' "$dest"
  fi
  chmod +x -- "$dest" || return 1
  version="$("$dest" --version 2>/dev/null || true)"
  printf 'OMP_VERSION %s\n' "${version:-missing}"
  if [ "$version" != "omp/18.3.5" ]; then
    printf 'STOP: installed file did not print omp/18.3.5\n' >&2
    return 1
  fi
}
course_install_omp
```

**Expected:** You see `KEEP:` or `INSTALLED`, and then `OMP_VERSION omp/18.3.5`. The verified download remains in its attempt folder.

**Stop:** Any STOP line appears, including a checksum miss, a shortcut destination, or a different existing file. The version line is anything other than `omp/18.3.5`.

**Recovery:** Leave both the download folder and any existing `"$HOME/.local/bin/omp"` in place. Do not delete the existing file, and do not rename the download onto it. For a checksum or download problem, paste the download step again and then paste this step again. For a different existing file or a shortcut, ask the device owner before anything is replaced. Do not switch to the musl asset to get past this stop.

## 7. Keep the user command folder on PATH

PATH is the list of folders your terminal searches when you type a command name. Ubuntu's default Bash startup file adds `"$HOME/.local/bin"` when that folder exists. This step adds that line only when the startup file does not already have it. It does not write the API key.

A terminal you open later reads the startup file. A terminal that is already open keeps its old PATH until you close it.

**Terminal: Ubuntu, ordinary user.**

```bash
course_persist_path() {
  local startup
  if [ -L "$HOME/.local/bin" ]; then
    printf 'STOP: %s is a symlink; the startup file was not changed\n' "$HOME/.local/bin" >&2
    return 1
  fi
  mkdir -p -- "$HOME/.local/bin" || return 1
  if [ -n "${BASH_VERSION:-}" ]; then
    startup="$HOME/.bashrc"
  elif [ -n "${ZSH_VERSION:-}" ]; then
    startup="$HOME/.zshrc"
  else
    printf 'STOP: open this guide in Bash or Zsh\n' >&2
    return 1
  fi
  if [ -L "$startup" ] || { [ -e "$startup" ] && [ ! -f "$startup" ]; }; then
    printf 'STOP: %s is not a regular file; it was not changed\n' "$startup" >&2
    return 1
  fi
  if [ -f "$startup" ] && grep -E -q '^[[:space:]]*(export[[:space:]]+)?PATH=.*\.local/bin' "$startup"; then
    printf 'PATH_LINE already present in %s\n' "$startup"
    return 0
  fi
  printf '%s\n' 'export PATH="$HOME/.local/bin:$PATH"' >> "$startup" || return 1
  printf 'PATH_LINE added to %s\n' "$startup"
}
course_persist_path
```

**Expected:** One line says `PATH_LINE already present` or `PATH_LINE added`, and it names `"$HOME/.bashrc"` for Bash or `"$HOME/.zshrc"` for Zsh.

**Stop:** You see a STOP line, or the named file is a shortcut.

**Recovery:** Do not write the key into the startup file. If the file is a shortcut, leave it and ask the device owner which ordinary file that terminal reads. Then open a new terminal from the desktop and paste this box there.

## 8. Use the course checkout

The course lives at `"$HOME/AI_Harness_Bootcamp"`. If that folder is absent, this step clones [the course repository](https://github.com/TheHolofex/AI_Harness_Bootcamp.git). If that folder is already a checkout of that exact origin, it is used as it is. Nothing is reset, pulled, or cleaned.

**Terminal: Ubuntu, ordinary user.**

```bash
course_use_checkout() {
  local origin_url
  R="$HOME/AI_Harness_Bootcamp"
  ORIGIN="https://github.com/TheHolofex/AI_Harness_Bootcamp.git"
  if [ -L "$R" ]; then
    printf 'STOP: %s is a symlink; it was not replaced\n' "$R" >&2
    return 1
  fi
  if [ ! -e "$R" ]; then
    git clone "$ORIGIN" "$R" || {
      printf 'STOP: clone failed; the path was not reused\n' >&2
      return 1
    }
  elif [ ! -d "$R" ]; then
    printf 'STOP: %s exists and is not a directory; it was not replaced\n' "$R" >&2
    return 1
  else
    origin_url="$(git -C "$R" remote get-url origin 2>/dev/null || true)"
    if [ "$origin_url" != "$ORIGIN" ]; then
      printf 'STOP: %s is not the course checkout; it was not changed\n' "$R" >&2
      return 1
    fi
    printf 'USE: existing checkout; no reset, pull, or clean\n'
  fi
  M="$R/reformation/AI_Harness_Bootcamp_2/module-00-setup"
  if [ ! -f "$R/reformation/shared/run_omp.py" ] || [ ! -f "$R/reformation/shared/course_guard.mjs" ] || [ ! -f "$M/scripts/verify-setup.sh" ] || [ ! -f "$M/shared/case/verify_tool_proof.py" ]; then
    printf 'STOP: this checkout is missing a course helper; it was not reset or updated\n' >&2
    return 1
  fi
  printf 'R %s\n' "$R"
  printf 'M %s\n' "$M"
}
course_use_checkout
```

**Expected:** You see `USE:` or a completed clone, then one `R` line and one `M` line. Both paths are under your home folder.

**Stop:** Any STOP line appears. The folder exists but is a different project, a file, or a shortcut.

**Recovery:** Do not delete, rename, reset, pull, or clean the existing folder. Leave it as it is and ask the person who owns it. A missing helper is not a reason to update the checkout from this guide. Clone help is in GitHub's [cloning a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) page.

## 9. Open a new terminal and confirm the install

Close this terminal completely. Open a new one from the desktop menu, not by typing `bash`, `sh`, or `su` in the old window. A program started from the old window is a child. A child can inherit exported variables and the old PATH. An independently opened terminal reads the startup file instead, and it does not inherit the old window's variables.

Do not export PATH in the new window before this check. The check is what shows whether the startup file worked.

**Terminal: Ubuntu, ordinary user, new window.**

```bash
course_confirm_new_terminal() {
  local resolved version
  resolved="$(command -v omp 2>/dev/null || true)"
  printf 'OMP_PATH %s\n' "${resolved:-missing}"
  if [ "$resolved" != "$HOME/.local/bin/omp" ]; then
    printf 'STOP: omp is not the user binary\n' >&2
    return 1
  fi
  version="$("$HOME/.local/bin/omp" --version 2>/dev/null || true)"
  printf 'OMP_VERSION %s\n' "${version:-missing}"
  if [ "$version" != "omp/18.3.5" ]; then
    printf 'STOP: version is not omp/18.3.5\n' >&2
    return 1
  fi
  if [ -n "${OPENROUTER_API_KEY:-}" ]; then
    printf 'SET\n'
    printf 'STOP: this window already has the key variable\n' >&2
    return 1
  fi
  printf 'MISSING\n'
}
course_confirm_new_terminal
```

**Expected:** `OMP_PATH` is your home folder plus `/.local/bin/omp`. `OMP_VERSION` is `omp/18.3.5`. The last line is `MISSING`.

**Stop:** The path is missing or points somewhere else, the version is not `omp/18.3.5`, or the key line is `SET`.

**Recovery:** For a missing or wrong `omp`, return to the PATH step in a window that can edit the startup file, then open another terminal from the desktop. Do not export PATH in the proof window to hide a miss. For `SET`, do not print the variable and do not treat `SET` as proof that the key was written to a file. Close this window. If you had opened it from the old terminal, open the next one from the desktop menu. If an independently opened window still prints `SET`, stop and follow [credentials](../shared/CREDENTIALS.md).

## 10. Enter the key

The next box is only the hidden read. Paste it, press Return, and wait. The terminal is waiting for the key even when it looks idle. Paste or type the key, then press Return. The characters do not appear. This stores the key in this process only. It does not write a profile, a file, or a log.

Do not put the key on the same line as a command. Do not run `echo`, `env`, `set`, or `printenv` to look at it. Read [credentials](../shared/CREDENTIALS.md) before you paste a key that may already have been exposed.

**Terminal: Ubuntu, ordinary user.**

```bash
IFS= read -r -s OPENROUTER_API_KEY
```

**Expected:** Nothing is echoed. After you press Return, the prompt comes back. It may stay on the same line, because hidden input does not print a newline.

**Stop:** Any character of the key appears on screen, or you pasted the key into the command box instead of waiting for the read.

**Recovery:** Treat a displayed key as exposed. Stop, follow [credentials](../shared/CREDENTIALS.md), and use the replacement key in a new window. Do not copy the displayed key into a file.

## 11. Export the key in this process

Export makes the variable available to programs you start from this window, including the proof. It still does not write the key to disk. `SET` means this process has a non-empty variable. It does not mean the key was saved, and it does not mean a file leak. `MISSING` means this process does not have it.

**Terminal: Ubuntu, ordinary user.**

```bash
export OPENROUTER_API_KEY
if [ -n "${OPENROUTER_API_KEY:-}" ]; then
  printf 'SET\n'
else
  printf 'MISSING\n'
fi
```

**Expected:** The only new line is `SET`.

**Stop:** The line is `MISSING`, or any command prints the key itself.

**Recovery:** Paste the hidden-read box again, then paste this box again. Do not add the key to a startup file to make `SET` survive a new terminal. A new independent terminal is expected to print `MISSING` until you enter the key there.

## 12. Choose Python and the checkout again

This new window does not keep the variables from the window you closed. These two boxes set them again. The checkout box will not clone over an existing course folder, and it will not update one.

**Terminal: Ubuntu, ordinary user.**

```bash
course_resolve_python() {
  PY="$(for candidate in python3.12 python3 python; do "$candidate" -c 'import sys; sys.exit(1) if sys.version_info < (3, 12) else print(sys.executable)' 2>/dev/null && break; done)"
  if [ -n "$PY" ]; then
    printf 'PY %s\n' "$PY"
    "$PY" --version
    return 0
  fi
  printf 'STOP: no real Python executable is version 3.12 or newer\n' >&2
  return 1
}
course_resolve_python
```

**Expected:** A `PY` line and a Python version of 3.12 or newer.

**Stop:** The STOP line appears, or the version is below 3.12.

**Recovery:** Return to the package and Python steps in the install window. Do not point `PY` at a copy you downloaded outside Ubuntu's packages.

**Terminal: Ubuntu, ordinary user.**

```bash
course_use_checkout() {
  local origin_url
  R="$HOME/AI_Harness_Bootcamp"
  ORIGIN="https://github.com/TheHolofex/AI_Harness_Bootcamp.git"
  if [ -L "$R" ]; then
    printf 'STOP: %s is a symlink; it was not replaced\n' "$R" >&2
    return 1
  fi
  if [ ! -e "$R" ]; then
    git clone "$ORIGIN" "$R" || {
      printf 'STOP: clone failed; the path was not reused\n' >&2
      return 1
    }
  elif [ ! -d "$R" ]; then
    printf 'STOP: %s exists and is not a directory; it was not replaced\n' "$R" >&2
    return 1
  else
    origin_url="$(git -C "$R" remote get-url origin 2>/dev/null || true)"
    if [ "$origin_url" != "$ORIGIN" ]; then
      printf 'STOP: %s is not the course checkout; it was not changed\n' "$R" >&2
      return 1
    fi
    printf 'USE: existing checkout; no reset, pull, or clean\n'
  fi
  M="$R/reformation/AI_Harness_Bootcamp_2/module-00-setup"
  if [ ! -f "$R/reformation/shared/run_omp.py" ] || [ ! -f "$R/reformation/shared/course_guard.mjs" ] || [ ! -f "$M/scripts/verify-setup.sh" ] || [ ! -f "$M/shared/case/verify_tool_proof.py" ]; then
    printf 'STOP: this checkout is missing a course helper; it was not reset or updated\n' >&2
    return 1
  fi
  printf 'R %s\n' "$R"
  printf 'M %s\n' "$M"
}
course_use_checkout
```

**Expected:** `USE:` for an existing checkout, then `R` and `M` lines.

**Stop:** Any STOP line appears.

**Recovery:** Do not pull, reset, or clean the checkout to create a missing helper. Stop and ask the person who owns that folder.

## 13. Prepare a fresh proof attempt

The proof folder, the token, and the evidence folder are outside the course checkout. The token is created with Python's `secrets` module and saved as `run-token.txt` beside the proof folder, then copied into it. The evidence child is named but not created. The launcher creates that child. Do not create `from-omp.txt` yourself.

**Terminal: Ubuntu, ordinary user.**

```bash
course_prepare_proof() {
  local attempt token_bytes
  if [ -z "${PY:-}" ] || [ ! -x "${PY:-}" ]; then
    printf 'STOP: PY is not set in this terminal\n' >&2
    return 1
  fi
  attempt="module-00-$(date -u +%Y%m%dT%H%M%SZ)-$$"
  BASE="$HOME/course-evidence/reformation-qa/$attempt"
  if [ -e "$BASE" ] || [ -L "$BASE" ]; then
    printf 'STOP: %s already exists and was not reused\n' "$BASE" >&2
    return 1
  fi
  mkdir -p -- "$BASE/proof" || return 1
  mkdir -p -- "$BASE/receipts" || return 1
  EVIDENCE="$BASE/receipts/live-1"
  if [ -e "$EVIDENCE" ] || [ -L "$EVIDENCE" ]; then
    printf 'STOP: evidence path already exists\n' >&2
    return 1
  fi
  "$PY" -c 'import secrets; print(secrets.token_hex(16), end="")' > "$BASE/run-token.txt" || return 1
  token_bytes="$(wc -c < "$BASE/run-token.txt" | tr -d '[:space:]')"
  if [ "$token_bytes" -lt 16 ]; then
    printf 'STOP: token file is empty; nothing was sent to the model\n' >&2
    return 1
  fi
  cp -- "$BASE/run-token.txt" "$BASE/proof/run-token.txt" || return 1
  cat > "$BASE/proof/prompt.txt" << 'COURSE_PROMPT'
Read run-token.txt with the course_read tool. Then write only from-omp.txt with the course_write tool. The file contents must be the words omp works, one space, and the exact token text from run-token.txt. Do not write any other file.
COURSE_PROMPT
  if [ -e "$BASE/proof/from-omp.txt" ] || [ -L "$BASE/proof/from-omp.txt" ]; then
    printf 'STOP: from-omp.txt already exists; start a new attempt\n' >&2
    return 1
  fi
  printf 'PROOF %s\n' "$BASE/proof"
  printf 'TOKEN_OUTSIDE %s\n' "$BASE/run-token.txt"
  printf 'EVIDENCE_NOT_CREATED %s\n' "$EVIDENCE"
}
course_prepare_proof
```

**Expected:** Three lines, starting with `PROOF`, `TOKEN_OUTSIDE`, and `EVIDENCE_NOT_CREATED`. The evidence path is printed, and that folder does not exist yet. The token value is not printed.

**Stop:** A STOP line appears, or `from-omp.txt` already exists.

**Recovery:** Leave the existing attempt in place. Paste this box again. The new paste uses a new attempt folder. Do not copy an old `from-omp.txt` into the new proof folder.

## 14. Ask for one tool write

This command starts the course launcher. The launcher selects OpenRouter and `openrouter/anthropic/claude-sonnet-4.6`. It allows the model to read the proof folder and to write only `from-omp.txt`. The key is read from this process. It is not placed on the command line.

A missing key exits 2 and does not create the evidence folder. A live failure exits 1. Keep that attempt. Do not run the launcher again against the same proof folder after a partial file exists.

**Terminal: Ubuntu, ordinary user.**

```bash
course_run_proof() {
  local status
  if [ -z "${PY:-}" ] || [ -z "${R:-}" ] || [ -z "${BASE:-}" ] || [ -z "${EVIDENCE:-}" ]; then
    printf 'STOP: proof paths are not set in this terminal\n' >&2
    return 1
  fi
  if [ -e "$EVIDENCE" ] || [ -L "$EVIDENCE" ]; then
    printf 'STOP: evidence already exists; start a new attempt\n' >&2
    return 1
  fi
  if [ -e "$BASE/proof/from-omp.txt" ] || [ -L "$BASE/proof/from-omp.txt" ]; then
    printf 'STOP: from-omp.txt already exists; start a new attempt\n' >&2
    return 1
  fi
  "$PY" "$R/reformation/shared/run_omp.py" \
    --workdir "$BASE/proof" \
    --prompt "$BASE/proof/prompt.txt" \
    --evidence "$EVIDENCE" \
    --allow-write from-omp.txt
  status="$?"
  printf 'LAUNCH_EXIT %s\n' "$status"
  if [ "$status" -eq 2 ]; then
    printf 'STOP: prerequisite hold; do not reuse this attempt\n' >&2
    return 2
  fi
  if [ "$status" -ne 0 ]; then
    printf 'STOP: live run failed; keep this attempt\n' >&2
    return 1
  fi
  return 0
}
course_run_proof
```

**Expected:** The launcher finishes, and the last line you added is `LAUNCH_EXIT 0`. The evidence folder now exists because the launcher created it.

**Stop:** `LAUNCH_EXIT 2` means a prerequisite hold. A missing key is that hold, and the evidence folder should still be absent. `LAUNCH_EXIT 1` means the live run failed or was incomplete. Any other STOP line means this attempt must not be reused.

**Recovery:** Do not create `from-omp.txt` by hand, and do not delete the attempt to make the same path work. For exit 2, paste the hidden-read box and the export box again in this window, then start again at the proof-prepare step so the folder is new. For exit 1, keep the attempt and start again at the proof-prepare step. Do not point the launcher at a second provider or a different model.

## 15. Check the proof

The checker reads the proof folder, the token file outside that folder, and the evidence folder. It passes only when `from-omp.txt` contains `omp works` and the token from this attempt, and when the evidence records that `course_write` wrote those bytes.

**Terminal: Ubuntu, ordinary user.**

```bash
course_verify_proof() {
  local status
  if [ -z "${PY:-}" ] || [ -z "${M:-}" ] || [ -z "${BASE:-}" ] || [ -z "${EVIDENCE:-}" ]; then
    printf 'STOP: proof paths are not set in this terminal\n' >&2
    return 1
  fi
  if [ ! -d "$EVIDENCE" ]; then
    printf 'STOP: evidence was not created; do not invent a proof file\n' >&2
    return 1
  fi
  "$PY" "$M/shared/case/verify_tool_proof.py" "$BASE/proof" "$BASE/run-token.txt" "$EVIDENCE"
  status="$?"
  printf 'VERIFY_EXIT %s\n' "$status"
  return "$status"
}
course_verify_proof
```

**Expected:** The checker prints `TOOL PROOF PASS`, and the last line is `VERIFY_EXIT 0`.

**Stop:** You see `TOOL PROOF HOLD`, `VERIFY_EXIT 1`, `VERIFY_EXIT 2`, or a STOP line.

**Recovery:** Do not edit `from-omp.txt`, and do not run the checker against a folder you filled in yourself. Keep this attempt. Return to the proof-prepare step for a new attempt. A later prerequisite report cannot replace this check.

## 16. Save the prerequisite report

This report checks the machine, the tools, the checkout, and whether the key variable is present in this process. It does not prove the live write. A checkout with changed or untracked files is not a failure and is not a reason to clean it.

**Terminal: Ubuntu, ordinary user.**

```bash
course_save_report() {
  local status
  if [ -z "${M:-}" ] || [ -z "${R:-}" ] || [ -z "${BASE:-}" ]; then
    printf 'STOP: report paths are not set in this terminal\n' >&2
    return 1
  fi
  if [ -e "$BASE/setup-report.txt" ] || [ -L "$BASE/setup-report.txt" ]; then
    printf 'STOP: report already exists; start a new attempt if you need another report\n' >&2
    return 1
  fi
  bash "$M/scripts/verify-setup.sh" "$R" "$BASE/setup-report.txt"
  status="$?"
  printf 'REPORT_EXIT %s\n' "$status"
  return "$status"
}
course_save_report
```

**Expected:** The command writes the report file it names. A run with no failed prerequisite prints `SETUP CHECK PASS` and `REPORT_EXIT 0`. The report does not contain the key.

**Stop:** The command prints `SETUP CHECK HOLD` or `REPORT_EXIT 1`. A line in the report tells you to pull, reset, or discard files.

**Recovery:** Read the first FAIL line and correct only that prerequisite. Do not pull, reset, clean, or discard the checkout because a report mentions changed files. Do not paste the key into the report. If the report passed but the proof check did not, the proof remains stopped.

## 17. Open the lab

The report is not the lab. Open [Give AI a clear, limited job](../shared/MODULE_00_LAB.md) in your browser. Use an ordinary text editor for the notes the lab asks you to write. The course files are in the folder printed as `R`.

**Expected:** The lab page opens and you can read its title.

**Stop:** The page is missing, or the browser opens a different folder than the `R` line from this terminal.

**Recovery:** From the `R` folder, open `reformation/AI_Harness_Bootcamp_2/module-00-setup/shared/MODULE_00_LAB.md` in your browser or editor. Do not clone a second copy to find it.
