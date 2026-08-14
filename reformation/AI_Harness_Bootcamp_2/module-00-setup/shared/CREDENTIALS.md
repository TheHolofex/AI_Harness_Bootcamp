# Connect the course accounts without leaking a key

This takes about 10 minutes. You will sign Codex in through its own login flow and load the shared xAI key only into the terminal process that needs it.

## Before you start

Keep keys in the password manager or secure handoff your organization approved. Do not paste a key into:

- a command after the prompt;
- a Markdown or text file;
- a shell profile such as `.zshrc`, `.bashrc`, or your PowerShell profile;
- Git configuration;
- a screenshot, chat, ticket, or course evidence record.

If a key has already appeared in any of those places, stop. Revoke it at the provider, remove the exposed copy, and use the replacement.

## Codex

**Terminal: the terminal named by your platform guide · normal user.**

Run:

```bash
codex login
```

Complete the browser flow your organization approved. Codex also supports API-key login, but the browser flow avoids placing a key in your terminal environment. Check the result:

```bash
codex login status
```

Both commands are typed exactly the same way in PowerShell.

Record the authentication **method**, not the credential. If the method is not the one you were told to use, run `codex logout` and sign in again.

Official source: [OpenAI Codex authentication](https://developers.openai.com/codex/auth).

## xAI for OpenCode and goose

Your platform guide gives one hidden-input command for its shell. The command must leave `XAI_API_KEY` in the current process without echoing the value. It is deliberately session-only. When you open a fresh terminal, you will enter it again.

A key that survives into a new terminal is a key you have written down somewhere — a shell profile, a tool's configuration file, a saved session — and every one of those copies can be read, synced, or committed later. Typing it again is the price of having exactly one copy, in the password manager.

After entering it with the hidden-input command in your platform guide, check only whether the variable exists:

**PowerShell:**

```powershell
if ([string]::IsNullOrWhiteSpace($env:XAI_API_KEY)) { 'MISSING' } else { 'SET' }
```

**Bash or zsh:**

```bash
if [ -n "${XAI_API_KEY:-}" ]; then printf 'SET\n'; else printf 'MISSING\n'; fi
```

The expected result is `SET`. Do not run `echo $XAI_API_KEY`, `Get-ChildItem Env:XAI_API_KEY`, `set`, `env`, or a diagnostic that dumps the environment.

OpenCode can store credentials through `/connect`. For this course, the xAI key lasts only until you close that terminal. Re-entering it in a new terminal proves that the key was not saved in a profile by mistake. goose also recognizes `XAI_API_KEY`; the guide sets provider and model without printing the key.

Official sources: [OpenCode providers](https://opencode.ai/docs/providers/) and [goose providers](https://goose-docs.ai/docs/getting-started/providers).

## Evidence you may save

Save only:

- `codex login status` with account identifiers redacted if present;
- `XAI_API_KEY: SET`;
- provider name and model ID;
- the tool versions;
- the proof-file contents.

A key value, even partly masked by a shell command you did not inspect, is not acceptable evidence.
