# Use one OpenRouter key without putting it in your work

Use your participant-supplied OpenRouter key for `openrouter/anthropic/claude-sonnet-4.6`. Set a provider-side per-key spending ceiling of US$40 before paid work. A local script cannot verify your account's ceiling or turn an SDK cost estimate into a bill.

Keep the key in your approved password manager. Do not put it in a prompt, command argument, file, shell profile, Git setting, screenshot, chat, ticket, or evidence record. The course launcher receives it through the current process environment and gives OMP an isolated configuration; it does not need another provider login.

## Enter the key through a hidden prompt

Choose the command for your terminal. Paste this command by itself, press Enter, then enter the key at the hidden prompt and press Enter again. Do not paste the export or conversion commands while the hidden prompt is waiting.

**Terminal: Bash or zsh, ordinary user.**

```bash
IFS= read -r -s OPENROUTER_API_KEY
```

**Terminal: PowerShell, ordinary user.**

```powershell
$secret = Read-Host 'OpenRouter key' -AsSecureString
```

**Expected:** The terminal accepts the key without displaying its value and returns to the ordinary prompt.

**Stop:** Characters are visible, the prompt is inaccessible with your access method, or you are unsure which program is receiving the input.

**Recovery:** Cancel the input and close that terminal. If the value was exposed, revoke it in OpenRouter and use a replacement. Ask for an accessible approved input method; do not turn off masking.

## Make it available only to this process and its children

Run the matching block only after the hidden-input command has finished. PowerShell briefly converts the secure string to the environment value required by the client, then zero-frees its unmanaged buffer and disposes the secure-string object.

**Terminal: Bash or zsh, ordinary user.**

```bash
export OPENROUTER_API_KEY
if [ -n "${OPENROUTER_API_KEY:-}" ]; then printf 'SET\n'; else printf 'MISSING\n'; fi
```

**Terminal: PowerShell, ordinary user.**

```powershell
$bstr = [IntPtr]::Zero
try {
  $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secret)
  $env:OPENROUTER_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
} finally {
  if ($bstr -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
  if ($secret) { $secret.Dispose() }
  Remove-Variable secret,bstr -ErrorAction SilentlyContinue
}
if ([string]::IsNullOrWhiteSpace($env:OPENROUTER_API_KEY)) { 'MISSING' } else { 'SET' }
```

**Expected:** Only `SET` is printed. That proves presence in this process, not validity, credit, model availability, or a successful provider call.

**Stop:** The result is `MISSING`, conversion fails, or any key value appears in output.

**Recovery:** Re-enter through the isolated hidden-input step. Revoke an exposed key before doing anything else. Never print the environment to troubleshoot credentials.

## Check a separately opened terminal

An independently opened terminal should not inherit a key from a terminal you previously used. A child shell started from that terminal can inherit its exported environment. Seeing `SET` alone therefore does not prove that a key was written to a profile or leaked.

**Terminal: Bash or zsh, ordinary user, independently opened window.**

```bash
if [ -n "${OPENROUTER_API_KEY:-}" ]; then printf 'SET\n'; else printf 'MISSING\n'; fi
```

**Terminal: PowerShell, ordinary user, independently opened window.**

```powershell
if ([string]::IsNullOrWhiteSpace($env:OPENROUTER_API_KEY)) { 'MISSING' } else { 'SET' }
```

**Expected:** `MISSING` in an independent window. Enter the key again there when you need a paid turn.

**Stop:** An unexpected `SET` needs an explanation before you claim that the lifecycle is process-only.

**Recovery:** Check how the terminal was launched and whether an approved parent process supplied the variable. Do not dump profiles or environment values into evidence. Revoke the key if you find an exposed or unauthorized persisted copy.

## End access when you finish

Closing the terminal removes its process environment. You can also remove the variable from the current process explicitly.

**Terminal: Bash or zsh, ordinary user.**

```bash
unset OPENROUTER_API_KEY
```

**Terminal: PowerShell, ordinary user.**

```powershell
Remove-Item Env:OPENROUTER_API_KEY -ErrorAction SilentlyContinue
```

**Expected:** The presence-only check now reports `MISSING` in that process.

**Stop:** A child process that already inherited the key may still hold its own copy. Environment removal does not revoke provider access.

**Recovery:** Close those processes. Revoke the provider key when access must end everywhere or a value was exposed.

Save provider/model identity, `omp/18.3.5`, `SET` or `MISSING`, and redacted run outcomes. Never save any part of the key. Process-local environment storage limits persistence; it is not protection from every other process running under your account.

Sources: [OpenRouter key settings](https://openrouter.ai/settings/keys), [Sonnet 4.6 through OpenRouter](https://openrouter.ai/anthropic/claude-sonnet-4.6), and [OMP model resolution at v18.3.5](https://github.com/can1357/oh-my-pi/blob/v18.3.5/docs/models.md).
