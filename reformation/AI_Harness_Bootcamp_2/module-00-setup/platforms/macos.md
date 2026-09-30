# Set up on macOS

Use this path on Apple Silicon or Intel macOS. You need Git, Python 3.12 or newer, the pinned OMP executable, a browser, and an ordinary text editor. Keep installation and class work separate. If device policy blocks an action, stop and use the [support packet](../shared/TROUBLESHOOTING.md); do not disable a protection to proceed.

## Check the machine and existing prerequisites

Open Terminal as your ordinary user. These checks make no model call.

**Terminal: macOS Terminal, Bash or zsh, ordinary user.**

```bash
uname -m
df -h "$HOME"
PY="$(for candidate in python3.12 python3 python; do "$candidate" -c 'import sys; sys.exit(1) if sys.version_info < (3, 12) else print(sys.executable)' 2>/dev/null && break; done)"
if [ -n "$PY" ]; then
  "$PY" --version && git --version
else
  printf 'HOLD: Python 3.12 or newer is not available.\n' >&2
  false
fi
```

**Expected:** The architecture is `arm64` or `x86_64`, at least 15 GB is available under your home directory, and Git and Python run. `PY` is the absolute path of a supported interpreter.

**Stop:** The architecture is unsupported, storage is insufficient, a prerequisite is absent, or macOS requests an installation you are not authorized to approve.

**Recovery:** Resolve the specific prerequisite. If Git and Python already work, keep them and skip the installation step below.

## Install missing Git or Python only when needed

If Homebrew is absent and you are authorized to install it, open [Homebrew's installation page](https://brew.sh/), read the displayed installation command, and follow its official prompts in Terminal. Apple Command Line Tools may require an installation dialog. Stop if you cannot approve it under your device policy. Do not improvise a privileged workaround.

Use the installed Homebrew location for your architecture, then install the two packages. This package step may request administrator approval through the official installer; OMP's user-bin installation later does not need it.

**Terminal: macOS Terminal, Bash or zsh, ordinary user; approve installation prompts only if authorized.**

```bash
if [ -x /opt/homebrew/bin/brew ]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
elif [ -x /usr/local/bin/brew ]; then
  eval "$(/usr/local/bin/brew shellenv)"
fi
if command -v brew >/dev/null 2>&1; then
  brew install git python@3.12 &&
  export PATH="$(brew --prefix python@3.12)/bin:$PATH"
else
  printf 'HOLD: complete the authorized Homebrew installation first.\n' >&2
  false
fi
```

**Expected:** Git and a supported Python are installed. Repeat the preceding prerequisite check to resolve `PY` and observe both versions.

**Stop:** The installer fails, policy blocks it, or the prerequisite check still fails.

**Recovery:** Save the first error and use the official [Homebrew installation guidance](https://docs.brew.sh/Installation) or your device owner. Do not run repeated unrelated installers.

## Download the exact OMP release into a new directory

Select the native macOS asset. Keep its checksum file beside it. The download block does not execute the downloaded program.

**Terminal: macOS Terminal, Bash or zsh, ordinary user.**

```bash
RUN="$(date -u +%Y%m%dT%H%M%SZ)-$$"
DOWNLOAD="$HOME/course-evidence/setup-macos-$RUN/download"
DEST="$HOME/.local/bin/omp"
case "$(uname -m)" in
  arm64) ASSET=omp-darwin-arm64 ;;
  x86_64) ASSET=omp-darwin-x64 ;;
  *) ASSET= ;;
esac
if [ -n "$ASSET" ]; then
  "$PY" -c "from pathlib import Path; import sys; Path(sys.argv[1]).mkdir(parents=True,exist_ok=False)" "$DOWNLOAD" &&
  curl --fail --location --output "$DOWNLOAD/$ASSET" "https://github.com/can1357/oh-my-pi/releases/download/v18.3.5/$ASSET" &&
  curl --fail --location --output "$DOWNLOAD/SHA256SUMS.txt" "https://github.com/can1357/oh-my-pi/releases/download/v18.3.5/SHA256SUMS.txt"
else
  printf 'HOLD: unsupported macOS architecture.\n' >&2
  false
fi
```

**Expected:** Both files exist in the new download directory and both downloads succeed. Their presence alone is not verification.

**Stop:** Either download fails, the destination exists, or a certificate/proxy error appears.

**Recovery:** Retain the failed directory. Resolve the network or path issue before choosing a new `RUN`; never disable certificate checks or execute a partial download.

## Verify before installation or first execution

The following script checks the exact selected filename against its unique SHA-256 entry. It installs only verified bytes. It refuses a symlink or a different existing destination; an identical verified file can be reused without replacement.

**Terminal: macOS Terminal, Bash or zsh, ordinary user.**

```bash
"$PY" - "$DOWNLOAD" "$ASSET" "$DEST" <<'PY'
from pathlib import Path
import hashlib, re, sys
folder, asset, target = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
entries = [line.split() for line in (folder / 'SHA256SUMS.txt').read_text().splitlines()]
expected = [parts[0] for parts in entries if len(parts) == 2 and parts[1].lstrip('*') == asset]
if len(expected) != 1 or not re.fullmatch(r'[0-9a-fA-F]{64}', expected[0]):
    raise SystemExit('HOLD: selected asset has no unique valid checksum entry.')
raw = (folder / asset).read_bytes()
actual = hashlib.sha256(raw).hexdigest()
if actual != expected[0].lower():
    raise SystemExit('HOLD: checksum mismatch; do not install or execute this file.')
if target.is_symlink() or (target.exists() and (not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != actual)):
    raise SystemExit('HOLD: a different destination exists; preserve it and resolve the installation conflict.')
target.parent.mkdir(parents=True, exist_ok=True)
if not target.exists():
    with target.open('xb') as output:
        output.write(raw)
target.chmod(target.stat().st_mode | 0o100)
print('SHA256 VERIFIED', asset, actual)
print('USER EXECUTABLE', target)
PY
```

**Expected:** `SHA256 VERIFIED` names the selected asset and actual digest. Only then is the verified user executable made runnable.

**Stop:** Any checksum, destination, write, or permission check fails.

**Recovery:** Preserve the failure. Do not delete or replace another installation to make this script succeed. Resolve the conflict deliberately or ask for support.

## Keep the verified executable available in a new terminal

`PATH` is the list of directories your shell searches for commands, from left to right. Your shell's profile is a text file it reads when a new login terminal opens. Add only the non-secret user-bin setting to the profile for the shell you are using. This command appends the setting once and leaves existing content in place.

**Terminal: macOS Terminal, Bash or zsh, ordinary user.**

```bash
if [ -n "${ZSH_VERSION-}" ]; then
  PROFILE="$HOME/.zprofile"
elif [ -n "${BASH_VERSION-}" ]; then
  PROFILE="$HOME/.bash_profile"
else
  PROFILE=
fi
if [ -n "$PROFILE" ]; then
  "$PY" - "$PROFILE" <<'PY'
from pathlib import Path
import sys
profile = Path(sys.argv[1])
if profile.is_symlink() or (profile.exists() and not profile.is_file()):
    raise SystemExit('HOLD: inspect the existing profile path before changing it.')
line = 'export PATH="$HOME/.local/bin:$PATH"'
existing = profile.read_text(encoding='utf-8') if profile.exists() else ''
if line not in existing.splitlines():
    with profile.open('a', encoding='utf-8') as stream:
        stream.write(('\n' if existing and not existing.endswith('\n') else '') + line + '\n')
print('PROFILE READY', profile)
PY
else
  printf 'HOLD: use the documented Bash or zsh terminal.\n' >&2
  false
fi
```

**Expected:** `PROFILE READY` names `.zprofile` for zsh or `.bash_profile` for Bash. The setting contains no credential.

**Stop:** The profile is linked, cannot be read or written, or an existing profile error prevents a new shell from opening normally.

**Recovery:** Preserve the file and first error. Inspect the existing profile with its owner; do not replace it with a downloaded profile or weaken device policy.

Put the same user-bin directory first for this terminal and run the verified executable.

**Terminal: macOS Terminal, Bash or zsh, ordinary user.**

```bash
export PATH="$HOME/.local/bin:$PATH"
command -v omp && omp --version
```

**Expected:** The resolved path is the verified user installation and the version is exactly `omp/18.3.5`.

**Stop:** Another executable is selected, the version differs, or macOS blocks execution.

**Recovery:** Inspect PATH or the specific macOS error. Follow authorized [Gatekeeper guidance](https://support.apple.com/en-us/102445); do not disable Gatekeeper or remove protections globally.

## Use the intended checkout without replacing existing work

Use one stable checkout location. Existing related work is not a reason to reset, pull, or clean it.

**Terminal: macOS Terminal, Bash or zsh, ordinary user.**

```bash
R="$HOME/AI_Harness_Bootcamp"
if [ ! -e "$R" ] && [ ! -L "$R" ]; then
  git clone https://github.com/TheHolofex/AI_Harness_Bootcamp.git "$R"
elif git -C "$R" rev-parse --is-inside-work-tree >/dev/null 2>&1 && [ "$(git -C "$R" remote get-url origin)" = https://github.com/TheHolofex/AI_Harness_Bootcamp.git ]; then
  printf 'Using the existing course checkout without changing it.\n'
else
  printf 'HOLD: the checkout path is occupied by unrelated or incomplete work.\n' >&2
  false
fi &&
M="$R/reformation/AI_Harness_Bootcamp_2/module-00-setup"
```

**Expected:** The intended checkout is available at `R`, with the Module 0 files under `M`.

**Stop:** Cloning fails or the existing path is unrelated/incomplete.

**Recovery:** Preserve that directory and ask the owner to resolve the path conflict. Do not hide a clone failure with `|| true` or discard local changes.

## Enter the key only after the hidden prompt is ready

Use your participant-supplied OpenRouter key, with the provider-side per-key spending ceiling set to US$40. Do not use a vendor login or another model. Paste this one command, press Enter, then enter the key without echo and press Enter again.

**Terminal: macOS Terminal, Bash or zsh, ordinary user.**

```bash
IFS= read -r -s OPENROUTER_API_KEY
```

**Expected:** The prompt returns without displaying the key.

**Stop:** The key appears, focus is uncertain, or hidden entry is inaccessible.

**Recovery:** Cancel and use the [credential handling procedure](../shared/CREDENTIALS.md). Revoke any exposed key. Do not paste the next block while the hidden read is waiting.

**Terminal: macOS Terminal, Bash or zsh, ordinary user.**

```bash
export OPENROUTER_API_KEY
if [ -n "${OPENROUTER_API_KEY:-}" ]; then printf 'SET\n'; else printf 'MISSING\n'; fi
```

**Expected:** Only `SET` is printed. This proves presence, not successful authentication or a model call.

**Stop:** The variable is missing or a secret value appears in output.

**Recovery:** Re-enter it through the isolated hidden prompt. Never save the key in a profile, command argument, or evidence file.

## Reopen independently, then make a token-bound tool proof

Open a new Terminal window from the application, not a child shell launched from the previous command prompt. Re-establish non-secret paths there. A child can inherit an exported key; `SET` alone is not proof of persistence or exposure.

**Terminal: macOS Terminal, Bash or zsh, ordinary user, independently opened window.**

```bash
R="$HOME/AI_Harness_Bootcamp"
M="$R/reformation/AI_Harness_Bootcamp_2/module-00-setup"
PY="$(for candidate in python3.12 python3 python; do "$candidate" -c 'import sys; sys.exit(1) if sys.version_info < (3, 12) else print(sys.executable)' 2>/dev/null && break; done)"
if [ -n "$PY" ] && [ "$(command -v omp)" = "$HOME/.local/bin/omp" ]; then
  command -v omp && omp --version &&
  if [ -n "${OPENROUTER_API_KEY:-}" ]; then printf 'SET\n'; else printf 'MISSING\n'; fi
else
  printf 'HOLD: the reopened terminal did not resolve the verified OMP and a supported Python.\n' >&2
  false
fi
```

**Expected:** OMP still resolves to the verified executable. An independent window ordinarily reports `MISSING` for the key.

**Stop:** Tool identity changes, Python cannot be resolved, or an unexpected inherited key is being mistaken for evidence of persistence.

**Recovery:** Inspect the non-secret profile setting in the previous step, then open another independent Terminal window and repeat the check. Do not repair PATH inside the verification block. Explain the process relationship, then enter the key using the two isolated blocks above in this window. Do not write it into a profile.

Create a fresh proof attempt. Its random token is class evidence, not a credential. The prompt receives the token only through a file inside the declared work root.

**Terminal: macOS Terminal, Bash or zsh, ordinary user.**

```bash
PROOF_RUN="$HOME/course-evidence/setup-proof-$(date -u +%Y%m%dT%H%M%SZ)-$$"
W="$PROOF_RUN/proof"
E="$PROOF_RUN/receipts"
TOKEN="$PROOF_RUN/run-token.txt"
"$PY" - "$PROOF_RUN" <<'PY'
from pathlib import Path
import secrets, sys
run = Path(sys.argv[1])
run.mkdir(parents=True, exist_ok=False)
work = run / 'proof'
work.mkdir()
token = secrets.token_hex(16)
(run / 'run-token.txt').write_text(token + '\n', encoding='utf-8')
(work / 'run-token.txt').write_text(token + '\n', encoding='utf-8')
(run / 'prompt.txt').write_text('Read run-token.txt with course_read. Use course_write to create from-omp.txt containing only omp works followed by one space and the exact token. Do not write another file.\n', encoding='utf-8')
print('FRESH PROOF WORK', work)
PY
```

**Expected:** Fresh proof work, token, and prompt exist. `E` does not exist yet.

**Stop:** The attempt already exists or preparation fails.

**Recovery:** Keep it and choose a new `PROOF_RUN`; never reuse a prior proof file as a new result.

**Terminal: macOS Terminal, Bash or zsh, ordinary user.**

```bash
"$PY" "$R/reformation/shared/run_omp.py" --workdir "$W" --prompt "$PROOF_RUN/prompt.txt" --evidence "$E" --allow-write from-omp.txt &&
"$PY" "$M/shared/case/verify_tool_proof.py" "$W" "$TOKEN" "$E"
```

**Expected:** A completed paid turn has the pinned identities, a successful `course_write`, exact disk contents, and `TOOL PROOF PASS`. The verifier does not accept the assistant's claim or a manually created file as sufficient evidence.

**Stop:** Missing key gives launcher exit 2 before a provider request. An incomplete turn or bad proof holds. A file left behind by a failed child is not success.

**Recovery:** Retain all output and receipts. Restore the missing prerequisite before creating a fresh proof attempt; do not switch provider, enable automatic retries, or reuse a partially written output.

## Save the prerequisite report separately

The setup report checks prerequisites and configuration presence. It does not replace the token-bound tool proof.

**Terminal: macOS Terminal, Bash or zsh, ordinary user.**

```bash
bash "$M/scripts/verify-setup.sh" "$R" "$PROOF_RUN/setup-report.txt"
```

**Expected:** The report records actual observations. A dirty checkout is informational; it is not a demand to discard work. Key or prerequisite failures remain `SETUP CHECK HOLD`.

**Stop:** A required check fails or the report destination already exists.

**Recovery:** Follow its specific next action and preserve the report. Use a new report filename after a real correction. Keep model-call failure, missing prerequisites, and unavailable native/accessible operations as distinct evidence limits.

Continue with [the bounded drafting assignment](../shared/MODULE_00_LAB.md) after the reachable prerequisites and actual proof are available. If a live prerequisite remains unavailable, retain the blocked lane rather than claim a completed tool proof.
