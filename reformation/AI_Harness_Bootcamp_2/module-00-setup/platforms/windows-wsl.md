# Windows WSL 2 with Ubuntu setup

This path uses Windows Subsystem for Linux 2 with the Ubuntu distribution so that all course work happens inside the Linux filesystem under your Linux home directory. Plan for 90 to 180 minutes if any Windows feature enable or reboot is needed. All course clone, work directories, evidence directories, and the Oh My Pi binary stay under the Linux `$HOME`. Never use `/mnt/c` for the course checkout or proof work. Never inherit a Windows `omp` binary, Windows config, or a Windows-saved key into the Ubuntu shell.

You need Git, Python 3.12 or newer inside Ubuntu, a browser, an ordinary text editor, and Oh My Pi 18.3.5 for Linux. The only provider key is `OPENROUTER_API_KEY`. The course launcher selects `openrouter/anthropic/claude-sonnet-4.6`. You do not install Node, npm, n8n, Obsidian, or another agent for this path.

The work splits into two parts that must not be mixed. First, any Windows-elevated steps required to enable WSL or install Ubuntu. Second, all remaining work inside an ordinary Ubuntu terminal as your normal Linux user. The elevated steps are only for the Windows side of the feature. After the first launch of Ubuntu you create your Linux username and password, and every later command is run from inside Ubuntu as that ordinary user.

If WSL is already present on the machine, inspect the installed distributions with `wsl -l -v` before any change. Never unregister a distribution. If the existing setup already points at Ubuntu and is set to WSL 2, proceed to the Ubuntu section. If it is set to WSL 1, the elevated step to change the default is shown below.

A checksum is a fingerprint of a file. You compare the fingerprint of the downloaded program with the fingerprint published beside it, and you do that before the program is allowed to run or before you make it executable.

The course checkout belongs at `$HOME/AI_Harness_Bootcamp`. An existing valid checkout of the course origin is used without reset, pull, or clean. A different folder at that path is left alone.

If a company policy or managed device blocks a Windows feature enable, stop and save the exact message. Do not bypass the block. When a step stops, start from the first failed check in [When setup stops](../shared/TROUBLESHOOTING.md).

## Windows side: enable WSL if it is not already present

These commands run in Windows PowerShell. Some require elevation. After any required reboot, return to an ordinary-user PowerShell to set the default and then launch Ubuntu for the first time.

**Terminal: Windows PowerShell, ordinary user.**

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsHardwareAbstractionLayer
```

**Expected:** a recent Windows version string and a build number of 19041 or higher.

**Stop:** the build is older than 19041 and no upgrade path is available.

**Recovery:** use the native PowerShell setup path on this machine or obtain a supported Windows version.

If WSL is not installed, the next command must be run from an elevated PowerShell (right-click the Start menu PowerShell entry and choose Run as administrator, or ask the person who supports the machine).

**Terminal: Windows PowerShell, elevated (Run as administrator).**

```powershell
wsl --install
```

**Expected:** the command enables the required Windows features, downloads the kernel, sets WSL 2 as default, and installs Ubuntu. A reboot prompt may appear.

**Stop:** a policy message blocks the feature enable, or the command prints help text instead of starting the install.

**Recovery:** if the command only prints help, run `wsl --list --online` to see available distributions and try `wsl --install -d Ubuntu`. If a policy or managed-device message blocks the enable, stop and save the exact text. Do not attempt to unregister or force an existing distribution.

If the install used the manual dism path instead, run these two lines while elevated.

**Terminal: Windows PowerShell, elevated (Run as administrator).**

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

**Expected:** both features report they are enabled or pending a reboot.

**Stop:** either command is denied by policy.

**Recovery:** save the denial message and stop.

Reboot the machine when prompted.

After the reboot, open an ordinary-user PowerShell and set the default to WSL 2.

**Terminal: Windows PowerShell, ordinary user.**

```powershell
wsl --set-default-version 2
wsl --update
wsl -l -v
```

**Expected:** the list shows at least one distribution (usually Ubuntu) with VERSION 2.

**Stop:** the list is empty or the version column shows 1 for the distribution you will use.

**Recovery:** if a distribution shows as version 1, run `wsl --set-version Ubuntu 2` (replace Ubuntu with the exact name shown). If the list is empty, return to the elevated install step.

Launch Ubuntu for the first time from the Start menu by typing "Ubuntu" or by running `wsl` from PowerShell. The first launch creates your Linux user and password. Nothing you type for the password is shown on screen.

**Terminal: first launch of Ubuntu (from Windows Start or wsl command).**

Follow the prompts to create a Linux username and password.

Then, still inside that first Ubuntu terminal, run:

```bash
whoami
pwd
cd "$HOME"
pwd
```

**Expected:** Your Linux username, then your Linux home directory, then the same home path after `cd "$HOME"`. The path must not start with `/mnt/c`.

**Stop:** `pwd` shows `/mnt/c` or a Windows path, or no username was created.

**Recovery:** type `cd "$HOME"` and run `pwd` again. If the distribution truly failed to create a user, stop without unregistering the distro and use the support packet. Never run `wsl --unregister` on an existing distribution.

From this point forward, every course command is run inside an Ubuntu terminal as your normal Linux user. Use the same Ubuntu terminal window, or open a new one with `wsl` or from the Start menu. All further sections assume you are inside that Ubuntu shell.

## Check the machine inside Ubuntu

You need enough free space under the Linux home and the matching Linux binary for the processor.

**Terminal: Ubuntu in WSL, ordinary Linux user.**

```bash
uname -m
df -h "$HOME"
```

**Expected:** `x86_64` (or `aarch64` if arm64 Linux), and at least 25 GB available under `$HOME`. The path printed by `df` must start with `/home/`, not `/mnt/c`.

**Stop:** low space, or the path is under `/mnt/c`.

**Recovery:** if the path is under `/mnt/c`, run `cd "$HOME"` and confirm with `pwd`. If space is low, free space inside the Linux filesystem. Do not move the work to `/mnt/c`.

## Install Git and Python inside Ubuntu

Git and Python come from Ubuntu's packages inside this Linux home. This step installs Git and the `python3.12` package. It does not upgrade every package on the machine, and it does not change security settings.

**Terminal: Ubuntu in WSL, ordinary Linux user.**

```bash
course_install_wsl_packages() {
  sudo apt update || return $?
  sudo apt install -y git python3.12 || return $?
  printf 'packages installed\n'
}
course_install_wsl_packages
```

**Expected:** apt finishes and the last line is `packages installed`.

**Stop:** apt prints an error, a policy message refuses the install, or the last line is not `packages installed`.

**Recovery:** Save the apt output. Do not run `sudo apt upgrade`, and do not change unattended upgrades or other machine-wide security settings. If apt says `python3.12` has no installation candidate, stop. This path does not add another package source.

## Choose the Python interpreter

Later steps call one real Python executable by its absolute path. That path is `PY`. This step keeps the first of `python3.12`, `python3`, or `python` that reports version 3.12 or newer through `sys.executable`. A version line from an older interpreter is not a pass.

**Terminal: Ubuntu in WSL, ordinary Linux user.**

```bash
course_resolve_python() {
  PY="$(for candidate in python3.12 python3 python; do "$candidate" -c 'import sys; sys.exit(1) if sys.version_info < (3, 12) else print(sys.executable)' 2>/dev/null && break; done)"
  if [ -n "$PY" ] && [ -x "$PY" ]; then
    printf 'PY %s\n' "$PY"
    "$PY" --version
    return 0
  fi
  printf 'STOP: no real Python executable is version 3.12 or newer\n' >&2
  return 1
}
course_resolve_python
```

**Expected:** A line starting with `PY ` gives an absolute path under your Linux home or `/usr`, and the next line starts with `Python 3.12` or newer.

**Stop:** You see the STOP line, no `PY` line, a version below 3.12, or a path that starts with `/mnt/c`.

**Recovery:** Return to the package step if `python3.12` was not installed. Do not point `PY` at a Windows Python under `/mnt/c`. Do not upgrade the whole system to get past this stop.

## Put the user bin on PATH inside Ubuntu

PATH is the list of folders this terminal searches when you type a command name. The export in this window lasts only until you close it. A later window finds `omp` only if a startup file that window actually reads contains the same line.

A login shell reads `$HOME/.profile`. An ordinary Ubuntu window in WSL is often not a login shell, and then Bash reads `$HOME/.bashrc` instead. This step adds one exact line to each of those two files, and only when that exact line is absent. Running it again does not add a second copy. It does not write the API key, and it does not delete anything under `$HOME/course-evidence`.

**Terminal: Ubuntu in WSL, ordinary Linux user.**

```bash
course_persist_wsl_path() {
  local line file
  line='export PATH="$HOME/.local/bin:$PATH"'
  if [ -L "$HOME/.local/bin" ]; then
    printf 'STOP: %s is a symlink; no startup file was changed\n' "$HOME/.local/bin" >&2
    return 1
  fi
  mkdir -p -- "$HOME/.local/bin" || return 1
  export PATH="$HOME/.local/bin:$PATH"
  for file in "$HOME/.profile" "$HOME/.bashrc"; do
    if [ -L "$file" ] || { [ -e "$file" ] && [ ! -f "$file" ]; }; then
      printf 'STOP: %s is not a regular file; it was not changed\n' "$file" >&2
      return 1
    fi
    if [ -f "$file" ] && grep -F -x -q -- "$line" "$file"; then
      printf 'PATH_LINE already present in %s\n' "$file"
      continue
    fi
    printf '%s\n' "$line" >> "$file" || return 1
    printf 'PATH_LINE added to %s\n' "$file"
  done
}
course_persist_wsl_path
```

**Expected:** Each of `.profile` and `.bashrc` prints either `PATH_LINE already present` or `PATH_LINE added`. This same window also has `$HOME/.local/bin` on PATH for the commands that follow here. That export is not the new-window proof.

**Stop:** A STOP line appears, or a permission error names either file.

**Recovery:** Confirm `whoami` is your normal Linux user, not root. If this window is root, close it and open Ubuntu as the normal user. Do not delete `$HOME/course-evidence`. Do not run an upgrade. If a startup file is a shortcut, leave it and ask the person who supports the machine which ordinary file that window reads.

## Download Oh My Pi and verify it before it can run

You download the selected Linux binary and `SHA256SUMS.txt` from the pinned release into a new directory that belongs only to this attempt. The published file lists a lowercase SHA-256 fingerprint, two spaces, then the exact filename. Nothing is moved into place and nothing is made executable unless that exact line matches the downloaded file.

The release page is [Oh My Pi v18.3.5](https://github.com/can1357/oh-my-pi/releases/tag/v18.3.5).

**Terminal: Ubuntu in WSL, ordinary Linux user.**

```bash
course_install_wsl_omp() {
  arch="$(uname -m)" || return 1
  case "$arch" in
    x86_64) asset=omp-linux-x64 ;;
    aarch64|arm64) asset=omp-linux-arm64 ;;
    *) printf 'HOLD: unsupported Linux architecture.\n' >&2; return 1 ;;
  esac
  download="$HOME/course-evidence/wsl-omp-$(date -u +%Y%m%dT%H%M%SZ)-$$/download"
  dest="$HOME/.local/bin/omp"
  "$PY" -c "from pathlib import Path; import sys; Path(sys.argv[1]).mkdir(parents=True,exist_ok=False)" "$download" || return 1
  base=https://github.com/can1357/oh-my-pi/releases/download/v18.3.5
  curl --fail --location --output "$download/$asset" "$base/$asset" || return 1
  curl --fail --location --output "$download/SHA256SUMS.txt" "$base/SHA256SUMS.txt" || return 1
  "$PY" - "$download" "$asset" "$dest" <<'PY'
from pathlib import Path
import hashlib, re, sys
folder, asset, target = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
entries = [line.split() for line in (folder/'SHA256SUMS.txt').read_text().splitlines()]
expected = [row[0] for row in entries if len(row)==2 and row[1].lstrip('*')==asset]
if len(expected)!=1 or not re.fullmatch(r'[0-9a-fA-F]{64}',expected[0]):
    raise SystemExit('HOLD: no unique valid checksum for selected asset')
raw = (folder/asset).read_bytes()
digest = hashlib.sha256(raw).hexdigest()
if digest != expected[0].lower():
    raise SystemExit('HOLD: checksum mismatch; do not execute')
if target.is_symlink() or (target.exists() and (not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest()!=digest)):
    raise SystemExit('HOLD: preserve the different existing destination')
target.parent.mkdir(parents=True,exist_ok=True)
if not target.exists():
    with target.open('xb') as output:
        output.write(raw)
target.chmod(target.stat().st_mode | 0o100)
print('SHA256 VERIFIED',asset,digest)
PY
  status=$?
  if [ "$status" -ne 0 ]; then return "$status"; fi
  "$dest" --version
}
course_install_wsl_omp
```

**Expected:** `SHA256 VERIFIED` identifies the selected Linux asset before first execution, followed by `omp/18.3.5`. The download folder remains as evidence. Only verified bytes become executable.

**Stop:** A download, checksum, destination, permission, or execution check fails. The function returns to your prompt without enabling persistent shell error-exit behavior.

**Recovery:** Keep the failed directory and existing installation. Resolve the specific error before using a new attempt; do not disable certificate checks, delete evidence, or run an unverified file.

## See the binary in this window

The export above is only for this window. It does not prove that a new window will find `omp`. That proof is the independent terminal later, and that later check must not export PATH first.

**Terminal: Ubuntu in WSL, ordinary Linux user.**

```bash
command -v omp
omp --version
```

**Expected:** `command -v` prints `$HOME/.local/bin/omp`, and the version line is `omp/18.3.5`.

**Stop:** `command -v` does not print that path, or the version is not `omp/18.3.5`.

**Recovery:** If `$HOME/.local/bin/omp` is missing, return to the download step. A new attempt keeps the old download folder. If a different `omp` is found earlier on PATH, do not overwrite it.

## Use the course checkout, or clone it once

The course lives at `$HOME/AI_Harness_Bootcamp`. An existing checkout of the course origin is used as it is. A different folder at that path is left alone. All paths stay inside the Linux home.

**Terminal: Ubuntu in WSL, ordinary Linux user.**

```bash
course_checkout_wsl() {
R="$HOME/AI_Harness_Bootcamp"
origin=https://github.com/TheHolofex/AI_Harness_Bootcamp.git
if [ -d "$R" ]; then
  if [ ! -d "$R/.git" ]; then
    echo "STOP: the home folder already has AI_Harness_Bootcamp, and it is not a Git checkout. It was not replaced."
    return 1
  fi
  remote=$(git -C "$R" remote get-url origin 2>/dev/null || true)
  if [ "$remote" != "$origin" ]; then
    echo "STOP: that checkout has a different origin. It was not replaced, reset, pulled, or cleaned."
    return 1
  fi
  echo "Using the existing course checkout."
else
  git clone "$origin" "$R"
  if [ $? -ne 0 ]; then
    echo "STOP: clone failed. No partial folder was cleaned up by this step."
    return 1
  fi
  echo "Cloned the course checkout."
fi
M="$R/reformation/AI_Harness_Bootcamp_2/module-00-setup"
lab="$M/shared/MODULE_00_LAB.md"
if [ ! -f "$lab" ]; then
  echo "STOP: this checkout does not contain the Module 0 lab. It was not reset, pulled, or cleaned."
  return 1
fi
echo "$R"
echo "$M"
}
course_checkout_wsl
```

**Expected:** either `Using the existing course checkout.` or `Cloned the course checkout.`, then the absolute course path and the Module 0 path.

**Stop:** the folder exists but is not the course origin, Git cannot read the origin, the clone fails, or the lab file is missing.

**Recovery:** leave the existing folder in place. If it is the wrong project, choose a different computer folder only with the person who supports your machine; do not delete, reset, pull, or clean this one. If the clone failed before creating the folder, run the block again. The clone URL is the course repository documented in [Cloning a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

`$R` and `$M` belong to this shell. The proof window sets `R`, `M`, and `PY` again. It cannot use a function that existed only here.

## Enter the key without showing it

The next command does nothing except wait for the key. Type the key at that hidden prompt and press Enter. Do not paste the key into the command, a file, a profile, or a chat. The rules for where a key must not go are in [Connect the course account without leaking a key](../shared/CREDENTIALS.md).

**Terminal: Ubuntu in WSL, ordinary Linux user.**

```bash
IFS= read -r -s OPENROUTER_API_KEY
```

**Expected:** the prompt returns, and the key does not appear as readable text.

**Stop:** the key appears in readable text, or you pasted it into the command line instead of the prompt.

**Recovery:** if the key was displayed or pasted into a command, revoke it with the provider, use the replacement, and run only this command again. Do not continue with a key that has been displayed.

## Load the key into this process only

This second command exports the variable for the current process and prints only `SET` or `MISSING`. The export happens in a separate command from the read. A child shell may inherit an exported variable, but `SET` alone never proves the key was persisted to a profile or leaked. `SET` by itself is never proof of a saved leak. `MISSING` in a completely new terminal is the check that this new process did not receive a saved key.

**Terminal: Ubuntu in WSL, ordinary Linux user.**

```bash
export OPENROUTER_API_KEY
if [ -n "${OPENROUTER_API_KEY:-}" ]; then printf 'SET\n'; else printf 'MISSING\n'; fi
```

**Expected:** `SET`.

**Stop:** `MISSING`, or any output that contains the key.

**Recovery:** run the hidden-read command again in this same shell, then run this export again. Do not check the key by printing the variable. Do not save it to `.profile` or any other file.

## Open an independent terminal and read the difference

A completely new Ubuntu terminal, opened from the Start menu Ubuntu entry or with `wsl` from a new PowerShell window, is a new process. It does not inherit the previous terminal's variables. Typing `bash` inside the window that has the key can inherit the variable. `SET` in that child does not prove the key was written to a profile.

Close the previous Ubuntu window only after you have seen `SET` there. Then open a brand new Ubuntu terminal. Do not export PATH in the new window before this check. If you export PATH first, `omp` can be found even when no startup file was read, and the check would not show persistence.

**Terminal: Ubuntu in WSL, ordinary Linux user, new window.**

```bash
course_confirm_wsl_terminal() {
  local resolved version status
  resolved="$(command -v omp || true)"
  printf 'OMP_PATH %s\n' "${resolved:-missing}"
  if [ "$resolved" != "$HOME/.local/bin/omp" ]; then
    printf 'STOP: this window did not find the user binary on its own PATH\n' >&2
    return 1
  fi
  version="$("$resolved" --version)"
  status=$?
  printf '%s\n' "${version:-missing}"
  printf 'omp exit %s\n' "$status"
  if [ "$status" -ne 0 ]; then
    return "$status"
  fi
  if [ "$version" != "omp/18.3.5" ]; then
    printf 'STOP: version is not omp/18.3.5\n' >&2
    return 1
  fi
  if [ -n "${OPENROUTER_API_KEY:-}" ]; then
    printf 'key in this window: SET — investigate\n'
    return 1
  fi
  printf 'key in this window: MISSING — expected\n'
}
course_confirm_wsl_terminal
```

**Expected:** `OMP_PATH` is your Linux home plus `/.local/bin/omp`. The next line is `omp/18.3.5`, then `omp exit 0`, then `key in this window: MISSING — expected`. This window did not export PATH before the check.

**Stop:** `OMP_PATH` is `missing` or any other path, the version is not `omp/18.3.5`, `omp exit` is not 0, or the key line is `SET`.

**Recovery:** If the path or version is wrong, do not export PATH in this window. That would hide the miss. Leave every folder under `$HOME/course-evidence` in place, including download logs. Run the path-miss block below, then open another new Ubuntu window and paste this check again. If this independent window prints `SET`, run the profile check before you enter a key. Do not print the variable. Do not upgrade packages.

**Terminal: Ubuntu in WSL, ordinary Linux user, new window, only after the path check stopped.**

```bash
course_note_wsl_path_miss() {
  local line file
  line='export PATH="$HOME/.local/bin:$PATH"'
  if [ -z "${BASH_VERSION:-}" ]; then
    printf 'STOP: this window is not Bash; no startup file was changed and no log was removed\n' >&2
    return 1
  fi
  if [ -x "$HOME/.local/bin/omp" ]; then
    printf 'selected '
    "$HOME/.local/bin/omp" --version
  else
    printf 'STOP: %s is missing or not executable; logs under %s were not removed\n' "$HOME/.local/bin/omp" "$HOME/course-evidence" >&2
    return 1
  fi
  if shopt -q login_shell; then
    file="$HOME/.profile"
    printf 'this window is a login shell\n'
  else
    file="$HOME/.bashrc"
    printf 'this window is not a login shell\n'
  fi
  if [ -L "$file" ] || { [ -e "$file" ] && [ ! -f "$file" ]; }; then
    printf 'STOP: %s is not a regular file; it was not changed and no log was removed\n' "$file" >&2
    return 1
  fi
  if [ -f "$file" ] && grep -F -x -q -- "$line" "$file"; then
    printf 'PATH_LINE already present in %s\n' "$file"
    printf 'STOP: the line is present, but this window still did not resolve omp from its own PATH. Do not export PATH here. No log was removed.\n' >&2
    return 1
  fi
  printf '%s\n' "$line" >> "$file" || return 1
  printf 'PATH_LINE added to %s\n' "$file"
  printf 'logs kept under %s\n' "$HOME/course-evidence"
}
course_note_wsl_path_miss
```

**Expected:** You see `selected omp/18.3.5`, whether this window is a login shell, and either `PATH_LINE added` or a STOP line that says the line is already present. Nothing under `$HOME/course-evidence` is deleted.

**Stop:** The selected binary is missing, the startup file is not a regular file, this window is not Bash, or the line is already present and `omp` is still not on this window's own PATH.

**Recovery:** Do not export PATH in this window, and do not delete download folders. If the line was just added, close this window, open a new Ubuntu window from the Start menu, and run the path check again with no PATH export. If the line was already present, save the printed lines and stop. Do not upgrade Ubuntu and do not change security settings.

## Set the course paths in this window

The window you closed kept `R`, `M`, and `PY`. This window does not have those variables, and it does not have the functions from the closed window. Set them here before any proof command. This block does not clone, reset, pull, or clean.

**Terminal: Ubuntu in WSL, ordinary Linux user, new window.**

```bash
course_assign_wsl_paths() {
  R="$HOME/AI_Harness_Bootcamp"
  M="$R/reformation/AI_Harness_Bootcamp_2/module-00-setup"
  if [ ! -f "$M/shared/MODULE_00_LAB.md" ]; then
    printf 'STOP: this window cannot see the Module 0 lab at %s. The checkout was not reset, pulled, or cleaned.\n' "$M" >&2
    return 1
  fi
  PY="$(for candidate in python3.12 python3 python; do "$candidate" -c 'import sys; sys.exit(1) if sys.version_info < (3, 12) else print(sys.executable)' 2>/dev/null && break; done)"
  if [ -z "$PY" ] || [ ! -x "$PY" ]; then
    printf 'STOP: no real Python executable is version 3.12 or newer\n' >&2
    return 1
  fi
  printf 'R %s\n' "$R"
  printf 'M %s\n' "$M"
  printf 'PY %s\n' "$PY"
  "$PY" --version
}
course_assign_wsl_paths
```

**Expected:** An `R` line, an `M` line, and a `PY` line with absolute paths, then a Python version of 3.12 or newer. `R` is under your Linux home, not under `/mnt/c`.

**Stop:** A STOP line appears, a path starts with `/mnt/c`, or the Python version is below 3.12.

**Recovery:** If the lab file is missing, paste the checkout block in this window. Do not delete or replace the home folder. If Python is missing, return to the package step. Do not call a function that existed only in the closed window.

## Check for a saved key without displaying it

Run this only when the independent terminal printed `SET` before you typed a key. It looks for the variable name in shell profiles and does not print a value.

**Terminal: Ubuntu in WSL, ordinary Linux user.**

```bash
found=0
for f in "$HOME/.profile" "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.zshrc"; do
  if [ -f "$f" ] && grep -q 'OPENROUTER_API_KEY' "$f"; then
    echo "STOP: a shell profile names the key variable. The line was not printed."
    found=1
  fi
done
if [ "$found" -eq 0 ]; then
  echo "No profile reference was found."
fi
```

**Expected:** if you reached this command because the new terminal printed `SET`, the script stops with a profile message. If you ran it after a correct `MISSING`, the line is `No profile reference was found.`

**Stop:** a profile reference exists. Also stop if the independent terminal printed `SET` but this check finds nothing: something else is supplying the variable, and you still must not print it.

**Recovery:** revoke the key at the provider. Edit the named profile in an editor to remove the assignment without copying the value, then confirm a new terminal prints `MISSING`.

## Enter the key again in the proof shell

The proof runs in this independent window, after that window has printed the persisted `omp` path without an extra PATH export. The key does not come along. Repeat the hidden read, then the separate export. Do not skip the read and paste the key into the export command.

**Terminal: Ubuntu in WSL, ordinary Linux user.**

```bash
IFS= read -r -s OPENROUTER_API_KEY
```

**Expected:** the prompt returns, and the key is not readable on screen.

**Stop:** the key is visible as readable text.

**Recovery:** revoke a displayed key, then run this read again.

**Terminal: Ubuntu in WSL, ordinary Linux user.**

```bash
export OPENROUTER_API_KEY
if [ -n "${OPENROUTER_API_KEY:-}" ]; then printf 'SET\n'; else printf 'MISSING\n'; fi
```

**Expected:** `SET`.

**Stop:** `MISSING`, or any output that contains the key.

**Recovery:** run the hidden read and this export again in this shell. Do not continue to the proof on `MISSING`.

## Create a fresh proof folder and token

The proof folder is outside the course checkout. This window must already have printed `R`, `M`, and `PY`. The token is created by Python's secrets module and stored outside the proof folder, then copied in so the model has to read it. The evidence folder is only a path at this point. You do not create it. You also do not create `from-omp.txt`.

**Terminal: Ubuntu in WSL, ordinary Linux user.**

```bash
course_prepare_wsl_proof() {
  local status
  if [ -z "${PY:-}" ] || [ ! -x "$PY" ]; then
    printf 'STOP: PY is not an executable path in this window\n' >&2
    return 1
  fi
  run="$HOME/course-evidence/setup-wsl-proof-$(date -u +%Y%m%dT%H%M%SZ)-$$"
  attempt="$run/module-00"
  proof="$attempt/proof"
  token_file="$attempt/run-token.txt"
  evidence="$attempt/receipts"
  prompt_file="$attempt/prompt.txt"
  "$PY" - "$attempt" <<'PY'
from pathlib import Path
import secrets, sys
attempt = Path(sys.argv[1])
attempt.mkdir(parents=True,exist_ok=False)
proof = attempt/'proof'
proof.mkdir()
token = secrets.token_hex(16) + '\n'
(attempt/'run-token.txt').write_text(token,encoding='utf-8')
(proof/'run-token.txt').write_text(token,encoding='utf-8')
(attempt/'prompt.txt').write_text('Read run-token.txt with course_read. Use course_write to create only from-omp.txt containing omp works, one space, and the exact token. Do not write another file.\n',encoding='utf-8')
print('FRESH PROOF WORK',proof)
print('EVIDENCE NOT PRECREATED',attempt/'receipts')
PY
  status=$?
  printf 'prepare exit %s\n' "$status"
  return "$status"
}
course_prepare_wsl_proof
```

**Expected:** `FRESH PROOF WORK` names the new work folder, `EVIDENCE NOT PRECREATED` names its absent receipt path, and the last line is `prepare exit 0`. The token value is not printed.

**Stop:** `PY` is unset, Python is missing, a path already exists, a file cannot be written, or `prepare exit` is not 0.

**Recovery:** Leave any partial attempt in place. Run the block again so it chooses new paths. Do not delete the course checkout or the download logs, and do not create the evidence folder or `from-omp.txt` by hand. If the STOP line says `PY` is unset, paste the path-assignment block in this window first.

## Ask for the one permitted write

The launcher runs the pinned Oh My Pi binary with permission to write only `from-omp.txt`. It reads the key from this process. Exit 2 means a prerequisite failed before the evidence folder was created. The `HOLD:` line names which prerequisite. A missing key is only one of those holds. Exit 1 means the live attempt failed after work began. Do not run the launcher a second time against a proof folder that already contains `from-omp.txt`.

**Terminal: Ubuntu in WSL, ordinary Linux user.**

```bash
course_run_wsl_proof() {
  local status
  if [ -z "${PY:-}" ] || [ ! -x "$PY" ] || [ -z "${R:-}" ] || [ -z "${proof:-}" ] || [ -z "${prompt_file:-}" ] || [ -z "${evidence:-}" ]; then
    printf 'STOP: this window is missing PY, R, or the proof paths\n' >&2
    return 1
  fi
  "$PY" "$R/reformation/shared/run_omp.py" --workdir "$proof" --prompt "$prompt_file" --evidence "$evidence" --allow-write from-omp.txt
  status=$?
  printf 'launcher exit %s\n' "$status"
  return "$status"
}
course_run_wsl_proof
```

**Expected:** The launcher's own output appears, and the last line is `launcher exit 0`. The evidence folder now exists because the launcher created it. That status is not yet the token-bound tool proof.

**Stop:** `launcher exit 2` with a `HOLD:` line means a prerequisite failed. The evidence folder should still be absent, and you must not invent the proof file. `launcher exit 1` means the live attempt failed. Exit 0 with no evidence folder is also a stop.

**Recovery:** Read the `HOLD:` line. Do not treat every exit 2 as a missing key. If that line says `OPENROUTER_API_KEY unavailable`, repeat the hidden read and the separate export in this window, then start again at the fresh-proof step so the paths are new. If it says `omp is not on PATH`, or that the pinned version did not match, return to the independent-terminal check. Do not export PATH here, and do not enter the key as that fix. If it says a directory is missing, already exists, or overlaps, keep the attempt and start again at the fresh-proof step. If it says `course_guard.mjs` is missing, the checkout is incomplete; do not reset, pull, or clean it. Exit 1 is a failed live attempt, not an authentication prompt. Do not delete `$HOME/course-evidence`, and do not write `from-omp.txt` yourself.

## Check the write against the token and the receipt

The checker takes the proof folder, the token file outside that folder, and the evidence folder. It passes only when `from-omp.txt` contains the words `omp works`, one space, and this run's token, and a `course_write` receipt matches the file on disk.

**Terminal: Ubuntu in WSL, ordinary Linux user.**

```bash
course_check_wsl_proof() {
  local status
  if [ -z "${PY:-}" ] || [ ! -x "$PY" ] || [ -z "${M:-}" ] || [ -z "${proof:-}" ] || [ -z "${token_file:-}" ] || [ -z "${evidence:-}" ]; then
    printf 'STOP: this window is missing PY, M, or the proof paths\n' >&2
    return 1
  fi
  checker="$M/shared/case/verify_tool_proof.py"
  "$PY" "$checker" "$proof" "$token_file" "$evidence"
  status=$?
  printf 'checker exit %s\n' "$status"
  return "$status"
}
course_check_wsl_proof
```

**Expected:** the checker's last result line is `TOOL PROOF PASS`, and the last line is `checker exit 0`.

**Stop:** the last result line is `TOOL PROOF HOLD`, `checker exit` is not 0, or the proof file is missing. A file you create by hand is not a pass.

**Recovery:** keep this attempt. Return to the fresh-proof step and use new folders. Do not edit `from-omp.txt` to make the words match. If the STOP line says `PY` or `M` is missing, paste the path-assignment block in this window first.

## Record prerequisites, not the live turn

This report checks that Git, Python, Oh My Pi, the checkout, and the key are present in this process. A passing report does not prove the live write. A dirty checkout is not a reason to reset, pull, or clean. The tool proof you already ran is the live-write check.

**Terminal: Ubuntu in WSL, ordinary Linux user.**

```bash
course_report_wsl_setup() {
  local status
  if [ -z "${R:-}" ] || [ -z "${M:-}" ] || [ -z "${attempt:-}" ]; then
    printf 'STOP: this window is missing R, M, or the attempt path\n' >&2
    return 1
  fi
  report="$attempt/setup-report.txt"
  bash "$M/scripts/verify-setup.sh" "$R" "$report"
  status=$?
  printf 'report exit %s\n' "$status"
  return "$status"
}
course_report_wsl_setup
```

**Expected:** a report file path, a last report line that begins `SETUP CHECK PASS` or `SETUP CHECK HOLD`, and then `report exit 0` or `report exit 1`. The report does not contain the key. The shell stays open.

**Stop:** the report path already exists, the report contains the key, or the command says `R` or `M` is missing. A hold in this report is a prerequisite hold. It is not repaired by editing the proof file, and a pass in this report does not replace `TOOL PROOF PASS`.

**Recovery:** fix the first failed prerequisite named in the report, then run this report command again only after choosing a new report path if the old file exists. Do not reset, pull, or clean the checkout because the report mentions local changes. Continue to the lab only after the tool proof printed `TOOL PROOF PASS`.

The next work is the [Module 0 lab](../shared/MODULE_00_LAB.md). The pins are in [Course setup pins](../shared/VERSIONS.md), and the cited install pages are collected in [Primary setup sources](../shared/SOURCES.md). If you are working on native Windows PowerShell instead of WSL, use [Windows PowerShell setup](windows-powershell.md) from the start rather than mixing the two paths.
