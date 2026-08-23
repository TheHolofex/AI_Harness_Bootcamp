#!/usr/bin/env bash
set -u

# Setup report for macOS, WSL, Ubuntu, and Arch Linux.
#
# Every check ends in one of three states:
#   PASS  the check ran and the observed value matched.
#   WARN  the check ran, the value is outside the expected set, the work can continue.
#   FAIL  the check ran and the value blocks later work, or the check could not run.
# A check that cannot run reports FAIL with the reason. Nothing degrades to PASS.
# Every non-PASS line carries a NEXT ACTION.
#
# Exit 0 when no check is FAIL. Exit 1 when any check is FAIL.
#
# The report names resolved paths so a stub earlier on PATH is visible, but it replaces
# the home directory with ~ and removes any credential embedded in a URL. No secret value
# is printed.

SELF="${BASH_SOURCE[0]:-$0}"
SCRIPT_DIR="$(cd -- "$(dirname -- "$SELF")" 2>/dev/null && pwd -P)" || SCRIPT_DIR="."
MODULE_DIR="$(cd -- "$SCRIPT_DIR/.." 2>/dev/null && pwd -P)" || MODULE_DIR="$SCRIPT_DIR/.."

ROOT_INPUT="${1:-$PWD}"
ROOT="$(cd -- "$ROOT_INPUT" 2>/dev/null && pwd -P)" || ROOT="$ROOT_INPUT"

EVIDENCE_DIR="${AHB_EVIDENCE_DIR:-$HOME/course-evidence/module-00}"
mkdir -p "$EVIDENCE_DIR" 2>/dev/null || true
RESULTS="${2:-$EVIDENCE_DIR/setup-report-$(date -u +%Y%m%dT%H%M%SZ)-$$.txt}"

ERR_FILE="$(mktemp "${TMPDIR:-/tmp}/ahb-verify.XXXXXX")" || ERR_FILE=""
cleanup() { [ -z "$ERR_FILE" ] || rm -f "$ERR_FILE"; }
trap cleanup EXIT

pass_count=0
warn_count=0
fail_count=0
lines=()

# ---------------------------------------------------------------------------- reporting

# Replace the home directory with ~ and strip any credential embedded in a URL.
HOME_MARK='~'
redact() {
  local s="${1-}"
  case "$s" in *://*@*) s="$(printf '%s' "$s" | sed -e 's#://[^/@[:space:]]*@#://***@#g')" ;; esac
  if [ -n "${HOME:-}" ]; then s="${s//"$HOME"/$HOME_MARK}"; fi
  printf '%s' "$s"
}

# A redacted path, or the word none when nothing was found.
or_none() {
  if [ -n "${1-}" ]; then redact "$1"; else printf 'none'; fi
}

record() {
  local state="$1" name="$2" detail="$3" action="${4:-}"
  local line="[$state] $name: $detail"
  if [ "$state" != PASS ]; then
    [ -n "$action" ] || action="Save this line and stop at this boundary; the troubleshooting guide starts from the first failed check."
    line="$line
        NEXT ACTION: $action"
  fi
  lines+=("$line")
  printf '%s\n' "$line"
  case "$state" in
    PASS) pass_count=$((pass_count + 1)) ;;
    WARN) warn_count=$((warn_count + 1)) ;;
    *) fail_count=$((fail_count + 1)) ;;
  esac
}

# ------------------------------------------------------------------- version comparison

# capture_version <name> <expected-or-empty-or-UNKNOWN> <command> [args...]
# Reads the version from standard output only. A tool that prints a warning to standard
# error still reports its real version.
capture_version() {
  local name="$1" expected="$2" cmd="$3"
  shift 3
  local resolved
  resolved="$(command -v "$cmd" 2>/dev/null)" || resolved=""
  if [ -z "$resolved" ]; then
    record FAIL "$name" "$cmd is not on PATH" \
      "Install $cmd with the step for it in your platform guide, open a new terminal, and run this check again."
    return
  fi
  local out status err first
  if [ -n "$ERR_FILE" ]; then
    out="$("$resolved" "$@" 2>"$ERR_FILE")"
    status=$?
    err="$(tr -d '\r' <"$ERR_FILE" | head -n 1)"
  else
    out="$("$resolved" "$@" 2>/dev/null)"
    status=$?
    err=""
  fi
  first="$(printf '%s' "$out" | head -n 1 | tr -d '\r')"
  if [ "$status" -ne 0 ]; then
    record FAIL "$name" "$(redact "$resolved") exited $status; first error line: ${err:-none}" \
      "Run $cmd ${*} in this terminal and read the error it prints."
    return
  fi
  if [ -z "$first" ]; then
    record FAIL "$name" "$(redact "$resolved") printed no version" \
      "Run $cmd ${*} in this terminal; a command that prints nothing is not the tool the course expects."
    return
  fi
  if [ "$expected" = UNKNOWN ]; then
    record WARN "$name" "observed $first at $(redact "$resolved"); the course pin table could not be read" \
      "Update your clone so the pin table is present, then run this check again."
    return
  fi
  if [ -n "$expected" ] && [ "$first" != "$expected" ]; then
    record WARN "$name" "course pin $expected, observed $first at $(redact "$resolved")" \
      "Write both versions in your setup notes, tell the instructor which one you have, and continue."
    return
  fi
  record PASS "$name" "$(redact "$resolved") — $first"
}

# ------------------------------------------------------------------------ course pins

read_pin() {
  local component="$1" file="$MODULE_DIR/shared/VERSIONS.md"
  [ -r "$file" ] || return 1
  sed -n -E "s/^\|[[:space:]]*${component}[[:space:]]*\|[[:space:]]*\`?([0-9][0-9.]*)\`?[[:space:]]*\|.*/\1/p" "$file" | head -n 1
}

pins_file="$MODULE_DIR/shared/VERSIONS.md"
pin_opencode="$(read_pin OpenCode 2>/dev/null)" || pin_opencode=""
pin_n8n="$(read_pin n8n 2>/dev/null)" || pin_n8n=""

# ------------------------------------------------------------------ platform and machine

case "$(uname -s)" in
  Darwin) platform="macOS" ;;
  Linux)
    if grep -qiE 'microsoft|wsl' /proc/version 2>/dev/null; then
      platform="WSL"
    elif [ -f /etc/arch-release ]; then
      platform="Arch"
    elif [ -r /etc/os-release ] && grep -q '^ID=ubuntu$' /etc/os-release; then
      platform="Ubuntu"
    else
      platform="unsupported"
    fi ;;
  *) platform="unsupported" ;;
esac
arch="$(uname -m)"
platform_ok=yes
case "$platform" in
  macOS) [[ "$arch" = arm64 || "$arch" = x86_64 ]] || platform_ok=no ;;
  Arch) [ "$arch" = x86_64 ] || platform_ok=no ;;
  Ubuntu|WSL) [[ "$arch" = x86_64 || "$arch" = aarch64 ]] || platform_ok=no ;;
  *) platform_ok=no ;;
esac
if [ "$platform_ok" = yes ]; then
  record PASS platform "$platform $arch"
else
  record FAIL platform "$platform $arch is not one of the five course paths" \
    "Use a machine the course supports, or send your operating system and architecture to the instructor before the session."
fi

disk_floor_gb=15
[ "$platform" != WSL ] || disk_floor_gb=25
free_kb="$(df -Pk "$HOME" 2>/dev/null | awk 'NR==2 {print $4}')"
if [ -z "${free_kb:-}" ]; then
  record FAIL disk.home "free space on the home directory could not be measured" \
    "Run df -h \$HOME in this terminal and read the Avail column."
else
  free_gb=$((free_kb / 1048576))
  if [ "$free_gb" -ge "$disk_floor_gb" ]; then
    record PASS disk.home "${free_gb} GB free at $(redact "$HOME") (course floor ${disk_floor_gb} GB)"
  else
    record FAIL disk.home "${free_gb} GB free at $(redact "$HOME"); the course floor is ${disk_floor_gb} GB" \
      "Free space until at least ${disk_floor_gb} GB is available, then run this check again."
  fi
fi

# An empty field in PATH means the current directory, so any command in the folder you
# happen to be standing in can be run instead of the real one.
path_rest="${PATH:-}"
path_index=1
path_empty=""
while :; do
  if [ -z "${path_rest%%:*}" ]; then
    path_empty="${path_empty:+$path_empty, }position $path_index"
  fi
  case "$path_rest" in
    *:*) path_rest="${path_rest#*:}" ;;
    *) break ;;
  esac
  path_index=$((path_index + 1))
done
if [ -z "$path_empty" ]; then
  record PASS path.empty "$path_index entries in PATH, none of them empty"
else
  record FAIL path.empty "PATH has an empty entry at $path_empty of $path_index; an empty entry means the current directory" \
    "Open the shell profile you edited in the PATH step of your platform guide, remove the stray colon, open a new terminal, and run this check again."
fi

# ------------------------------------------------------------------------------- tools

if [ -n "$pin_opencode" ] && [ -n "$pin_n8n" ]; then
  record PASS pins.source "OpenCode $pin_opencode and n8n $pin_n8n read from $(redact "$pins_file")"
else
  record FAIL pins.source "the course pin table at $(redact "$pins_file") is missing or has no version rows" \
    "Update your clone of the course repository, then run this check again."
  pin_opencode=UNKNOWN
  pin_n8n=UNKNOWN
fi

capture_version git '' git --version
capture_version node '' node --version
capture_version npm '' npm --version
capture_version codex '' codex --version
capture_version opencode "$pin_opencode" opencode --version
capture_version goose '' goose --version
capture_version n8n "$pin_n8n" n8n --version

npm_prefix="$(npm config get prefix 2>/dev/null)" || npm_prefix=""
case "$npm_prefix" in
  "$HOME"/*)
    if [ -w "$npm_prefix" ]; then
      record PASS npm.prefix "$(redact "$npm_prefix") is user-owned and writable"
    else
      record FAIL npm.prefix "$(redact "$npm_prefix") is not writable by you" \
        "Set the npm prefix to a directory inside your home, as the npm step in your platform guide does. Do not add sudo."
    fi ;;
  *)
    record FAIL npm.prefix "want a prefix under $(redact "$HOME"), observed ${npm_prefix:-none}" \
      "Set the npm prefix to a directory inside your home, as the npm step in your platform guide does, then open a new terminal and run this check again." ;;
esac

for tool in codex opencode n8n; do
  tool_path="$(command -v "$tool" 2>/dev/null)" || tool_path=""
  case "$tool_path" in
    "$npm_prefix"/*) record PASS "path.$tool" "$(redact "$tool_path")" ;;
    *) record FAIL "path.$tool" "want a command under $(redact "${npm_prefix:-the npm prefix}"), observed $(or_none "$tool_path")" \
        "Reinstall $tool with the global npm step in your platform guide, then open a new terminal and run this check again." ;;
  esac
done

goose_path="$(command -v goose 2>/dev/null)" || goose_path=""
case "$goose_path" in
  "$HOME/.local/bin/"*) record PASS path.goose "$(redact "$goose_path")" ;;
  *) record FAIL path.goose "want ~/.local/bin/goose, observed $(or_none "$goose_path")" \
      "Reinstall goose with the installer step in your platform guide, then open a new terminal and run this check again." ;;
esac

node_major="$(node -p 'Number(process.versions.node.split(".")[0])' 2>/dev/null)" || node_major=""
node_resolved="$(command -v node 2>/dev/null)" || node_resolved=""
if [ -z "$node_major" ] || ! printf '%s' "$node_major" | grep -Eq '^[0-9]+$'; then
  record FAIL runtime.node "the running Node version could not be read" \
    "Run node --version in this terminal and read the error it prints."
elif [ "$node_major" -eq 24 ]; then
  record PASS runtime.node "Node 24.x at $(redact "$node_resolved")"
else
  record FAIL runtime.node "want Node 24.x, observed ${node_major}.x at $(redact "${node_resolved:-none}")" \
    "Install Node 24 with the step in your platform guide and make it the first node on PATH, then open a new terminal and run this check again."
fi

python_cmd=""
for candidate in python3.12 python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then python_cmd="$candidate"; break; fi
done
if [ -z "$python_cmd" ]; then
  record FAIL runtime.python "Python is not on PATH" \
    "Install Python 3.12 or newer with the step in your platform guide, then open a new terminal and run this check again."
else
  python_resolved="$(command -v "$python_cmd" 2>/dev/null)" || python_resolved=""
  python_version="$("$python_resolved" --version 2>/dev/null | head -n 1 | tr -d '\r')"
  "$python_resolved" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)' >/dev/null 2>&1
  python_status=$?
  if [ "$python_status" -eq 0 ]; then
    record PASS runtime.python "${python_version:-version not printed} at $(redact "$python_resolved")"
  elif [ "$python_status" -eq 1 ]; then
    record FAIL runtime.python "want Python 3.12 or newer, observed ${python_version:-no version} at $(redact "$python_resolved")" \
      "Install Python 3.12 or newer with the step in your platform guide and put it ahead of the older one on PATH, then open a new terminal and run this check again."
  else
    record FAIL runtime.python "$(redact "$python_resolved") did not run; exit status $python_status" \
      "Run $python_cmd --version in this terminal and read the error it prints."
  fi
fi

# ---------------------------------------------------------------------- course clone

if ! command -v git >/dev/null 2>&1; then
  record FAIL repo.clone "git is not on PATH, so the course clone could not be read" \
    "Install git with the step in your platform guide, open a new terminal, and run this check again."
elif [ -d "$ROOT/.git" ]; then
  remote="$(git -C "$ROOT" remote get-url origin 2>/dev/null)" || remote=""
  revision="$(git -C "$ROOT" rev-parse --verify HEAD 2>/dev/null)" || revision=""
  dirty="$(git -C "$ROOT" status --porcelain 2>/dev/null)" || dirty=""
  if [ "$remote" = 'https://github.com/TheHolofex/AI_Harness_Bootcamp.git' ]; then
    record PASS repo.remote "$remote"
  else
    record FAIL repo.remote "want the course HTTPS origin, observed $(or_none "$remote")" \
      "Point origin at the course repository over HTTPS, or clone it again into a new directory, then run this check again."
  fi
  if printf '%s' "$revision" | grep -Eq '^[0-9a-f]{40}$'; then
    record PASS repo.revision "${revision:0:12}"
  else
    record FAIL repo.revision "no commit is checked out in $(redact "$ROOT")" \
      "Run git log -1 in the repository root and read the error it prints."
  fi
  if [ -z "$dirty" ]; then
    record PASS repo.clean "no changed or untracked paths"
  else
    dirty_count="$(printf '%s\n' "$dirty" | grep -c .)"
    record FAIL repo.clean "$dirty_count changed or untracked paths in the clone" \
      "Run git status --short in the repository root, then move your own files out of the clone or discard the changes. The clone must stay as cloned."
  fi
else
  record FAIL repo.clone "$(redact "$ROOT") is not a Git worktree" \
    "Change to the course repository directory and run this check again from there."
fi

missing_module=""
for required in shared/MODULE_00_LAB.md shared/VERSIONS.md shared/case/verify_tool_proof.py shared/case/verify_n8n.py platforms; do
  [ -e "$MODULE_DIR/$required" ] || missing_module="${missing_module:+$missing_module, }$required"
done
case "$MODULE_DIR" in
  "$ROOT"/*) module_in_root=yes ;;
  *) module_in_root=no ;;
esac
if [ -n "$missing_module" ]; then
  record FAIL repo.module "this clone is missing $missing_module under $(redact "$MODULE_DIR")" \
    "Run git pull in the repository root to get the current course files, then run this check again."
elif [ "$module_in_root" = no ]; then
  record FAIL repo.module "the checks you are running live in $(redact "$MODULE_DIR"), which is outside $(redact "$ROOT")" \
    "Run this check from the repository root you cloned, using the copy of the script inside that clone."
else
  record PASS repo.module "the course files for this session are present at $(redact "$MODULE_DIR")"
fi

# --------------------------------------------------------------- credentials and auth

if [ -n "${XAI_API_KEY:-}" ]; then
  record PASS secret.xai "SET in current process; value not printed"
else
  record FAIL secret.xai "MISSING in current process" \
    "Enter the key again with the hidden-input step in your platform guide, in this same terminal, then run this check again."
fi

if [ "${GOOSE_PROVIDER:-}" = xai ] && [ -n "${GOOSE_MODEL:-}" ]; then
  record PASS config.goose "provider=xai model=$GOOSE_MODEL"
else
  record FAIL config.goose "provider=${GOOSE_PROVIDER:-unset} model=${GOOSE_MODEL:-unset}" \
    "Export GOOSE_PROVIDER and GOOSE_MODEL with the values in your platform guide, in this same terminal, then run this check again."
fi

if command -v codex >/dev/null 2>&1; then
  if codex login status >/dev/null 2>&1; then
    record PASS auth.codex "login-status command passed; account details not copied"
  else
    record FAIL auth.codex "codex login status returned a non-zero exit status" \
      "Run codex login status in this terminal and read its message before signing in again."
  fi
else
  record FAIL auth.codex "codex is not on PATH, so its sign-in state could not be read" \
    "Install codex with the step in your platform guide, open a new terminal, and run this check again."
fi

# -------------------------------------------------------------------- WSL-only checks

if [ "$platform" = WSL ]; then
  if [ -r /etc/os-release ]; then . /etc/os-release; fi
  case "${ID:-}:${VERSION_ID:-}" in
    ubuntu:24.04|ubuntu:26.04) record PASS wsl.release "${PRETTY_NAME:-Ubuntu ${VERSION_ID:-}}" ;;
    *) record FAIL wsl.release "the course WSL path runs on Ubuntu 24.04 or 26.04, observed ${PRETTY_NAME:-unknown}" \
        "Install the Ubuntu 24.04 or 26.04 distribution with the WSL step in your guide and run the course work inside it." ;;
  esac
  case "$ROOT" in
    "$HOME"/*) record PASS wsl.location "$(redact "$ROOT") is under the Linux home directory" ;;
    *) record FAIL wsl.location "the clone is at $(redact "$ROOT"), outside the Linux home directory" \
        "Clone the repository again under your Linux home directory and work only from there." ;;
  esac
  mixed=no
  for tool in git node npm codex opencode goose n8n; do
    tool_path="$(command -v "$tool" 2>/dev/null)" || tool_path=""
    case "$tool_path" in
      /mnt/*|*.exe|*.cmd)
        record FAIL "wsl.path.$tool" "$tool resolves to the Windows tool at $(redact "$tool_path")" \
          "Install $tool inside Ubuntu with the step in your WSL guide, so the Linux copy is found first."
        mixed=yes ;;
    esac
  done
  [ "$mixed" = yes ] || record PASS wsl.paths "all required commands resolve to Linux paths"
fi

# ----------------------------------------------------------------- Ubuntu-only checks

if [ "$platform" = Ubuntu ]; then
  if [ -r /etc/os-release ]; then . /etc/os-release; fi
  case "${VERSION_ID:-}" in
    24.04|26.04) record PASS ubuntu.release "${PRETTY_NAME:-Ubuntu ${VERSION_ID:-}}" ;;
    *) record FAIL ubuntu.release "the course Ubuntu path runs on 24.04 or 26.04 LTS, observed ${PRETTY_NAME:-unknown}" \
        "Use an Ubuntu 24.04 or 26.04 LTS machine, or tell the instructor which release you have before the session." ;;
  esac
  if [ -n "${XDG_CURRENT_DESKTOP:-}" ] || [ -n "${DISPLAY:-}" ] || [ -n "${WAYLAND_DISPLAY:-}" ]; then
    record PASS desktop.session "desktop session detected"
  else
    record FAIL desktop.session "no desktop session; the Obsidian step cannot run on this machine" \
      "Run the Obsidian step on a machine with a desktop, or record this limit and send it to the instructor before the session."
  fi
fi

# ------------------------------------------------------------------------------ verdict

if [ "$fail_count" -eq 0 ]; then
  verdict="SETUP CHECK PASS — ${pass_count} PASS, ${warn_count} WARN, ${fail_count} FAIL"
else
  verdict="SETUP CHECK HOLD — ${pass_count} PASS, ${warn_count} WARN, ${fail_count} FAIL"
fi

{
  printf 'AI Harness Bootcamp setup report\n'
  printf 'Generated: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'Platform: %s %s\n' "$platform" "$arch"
  printf 'Root: %s\n\n' "$(redact "$ROOT")"
  printf '%s\n' "${lines[@]}"
  printf '\n%s\n' "$verdict"
} >"$RESULTS"

printf '\n%s — report: %s\n' "$verdict" "$RESULTS"
if [ "$fail_count" -eq 0 ]; then
  exit 0
fi
exit 1
