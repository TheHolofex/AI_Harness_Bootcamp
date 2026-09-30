# When setup stops

Start with the first failed action. Save its exact error and the last known-good observation before changing anything. Do not reinstall every tool or discard an existing checkout.

## Choose the next action from the observed failure

| Observation | Next action |
|---|---|
| Git or Python is missing | Return to the named platform's prerequisite step. On a managed device, stop when policy blocks installation and send the support packet below. |
| A download fails | Keep the HTTP, proxy, or certificate error. Use the official release URLs. Do not disable TLS verification or execute an incomplete download. |
| The checksum fails or the selected asset has no unique checksum entry | Do not install or execute the binary. Retain the failed download separately and investigate the filename, release, and source before downloading into a new directory. |
| `omp` is not found | Check the resolved command path below. Add only the user-bin directory named by your platform guide, then check again in the intended terminal. |
| `omp` reports a different version | Keep the observed path and version. Do not overwrite a different installation silently. Use the verified course binary and confirm that PATH resolves to it. |
| A course directory already exists | Confirm that it is the intended checkout. Use it without reset, pull, or clean when it is valid; otherwise leave it untouched and resolve the path conflict. |
| The new terminal has tools but the key is `MISSING` | This is expected for independently opened terminals. Enter the key through the hidden-input step in that terminal. Never put the key in a shell profile. |
| A new process reports an unexpected `SET` | Determine whether it inherited the environment from a parent. `SET` alone does not prove persistence or exposure. Do not dump the environment into evidence. |
| The launcher exits 2 | Read its prerequisite message. Missing key, wrong OMP version, missing input, conflicting permissions, or an existing attempt can stop before a provider request. No live success has occurred. |
| The launcher exits 1 | Retain the entire attempted run. Inspect `result.json` and the raw receipts; an incomplete turn is not rescued by a file left behind. |
| The provider returns 401 or 403 | Confirm the participant key and model access in OpenRouter without printing the key. Do not try a direct-provider login or silently switch models. |
| The provider returns 402, a spending-limit error, or 429 | Stop paid work. Preserve the response and resolve credit, the approved limit, or rate availability before an explicit new attempt. Do not raise the spending ceiling or loop retries. |
| The assistant claims it wrote a file, but the file or receipt is absent | Record `HOLD`. Check the declared work root and authorized filename. Do not manufacture the file or substitute chat text as a tool-write receipt. |
| A write or evidence destination already exists | Preserve that attempt. Start with new work/output and receipt paths after documenting the cause; changing only E does not make an existing output new. |
| A Windows script is blocked by managed execution policy | Save the policy error and ask the device owner. Do not bypass organizational policy or request broad machine-wide weakening. |
| WSL paths point under `/mnt/c` | Use the Linux home directory and Linux OMP asset in Ubuntu. Do not mix Windows executable/configuration paths with the WSL attempt. |

## Confirm the command you are actually running

These checks make no provider call and print no credential. Run the block in the same terminal that failed.

**Terminal: Bash or zsh, ordinary user.**

```bash
command -v omp && omp --version
```

**Terminal: PowerShell, ordinary user.**

```powershell
$ompCommand = Get-Command omp -CommandType Application -ErrorAction Stop
$ompCommand.Source
& $ompCommand.Source --version
```

**Expected:** The path is the installation you verified, and the version is exactly `omp/18.3.5`.

**Stop:** The command is missing, resolves to an unexpected installation, fails to run, or reports another version.

**Recovery:** Correct only the installation or PATH issue identified by the output. Preserve other installations and repeat the check before a paid turn.

**PATH** is the ordered list of directories searched for a command name. Changing it does not install a program, and an already open terminal does not automatically receive later configuration changes. Credential variables have a different lifecycle: keep the key process-local even if you save a non-secret PATH setting.

## Distinguish slow work from a stopped process

Keep the original terminal visible. Use Activity Monitor on macOS, Task Manager on Windows, or your Linux system monitor to inspect the named download or package-manager process and its current CPU, disk, and network activity. No activity in one observation is not proof of a hang.

Follow the package manager's own recovery instructions if installation was interrupted; do not kill or restart a transaction blindly. For a provider turn, the launcher has a bounded timeout and records an incomplete attempt. Let that boundary report the failure rather than launch a second paid process to see whether it is faster.

## Capture a support packet

```text
Platform, version, and architecture:
Terminal and privilege level:
Step title:
Command or UI action, with no key value:
Resolved tool path and version:
First error and exit code:
Expected observation:
Last known-good observation:
What changed immediately before the failure:
External attempt/report location:
Whether any output or forbidden effect appeared:
```

Redact personal paths, account IDs, internal hosts, and credentials from the copy you share. Keep command names, versions, exit codes, and the first error. An exposed key must be revoked; deleting it from a screenshot does not revoke access.

Make one targeted correction and repeat the failed check. If a correction cannot be explained, a rollback fails, or device policy blocks the action, record `HOLD` and contact the responsible owner. Do not disable certificate checks, Gatekeeper, antivirus, or protected filesystem permissions to force progress.
