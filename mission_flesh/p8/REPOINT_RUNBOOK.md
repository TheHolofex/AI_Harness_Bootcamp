# Re-point runbook — Codex app to the open endpoint

Re-pointing means changing where the Codex app sends its requests: the same app, the same project, and the same harness, now talking to a hosted open model at a different address instead of the course home model, `gpt-5.6-terra`. Nothing else about your setup moves — which is the whole test, because everything you built should keep working when only the engine changes. You can read this page and stage every edit before the real endpoint details exist; only the placeholder swap waits on the pin posted this morning.

## The file you edit

The app reads its configuration from `%USERPROFILE%\.codex\config.toml` — the same file where `forced_login_method = "api"` and `model = "gpt-5.6-terra"` already live. Edit that file at that path; a `.codex\config.toml` inside a project folder cannot do this job, because provider definitions there are ignored and must live in the user-level file. Before you change anything, make a byte-for-byte backup:

```powershell
Copy-Item "$env:USERPROFILE\.codex\config.toml" "$env:USERPROFILE\.codex\config.toml.p8-backup"
```

The backup is your rollback. Record the old model and provider values in your re-point note as the old-value evidence.

## The provider block

Two additions, in two different places — and the placement is TOML law, not tidiness. In TOML, every line below a `[bracketed]` header belongs to that header's table, so a table pasted above the file's existing lines silently swallows them: they still read fine in the file, but they stop being root keys and stop doing their jobs. `forced_login_method = "api"` is exactly such a line, and losing it quietly re-opens the ChatGPT-login door the install guide closed.

First, at the very top of the file — line 1, above everything already there:

```toml
model = "YOUR_MODEL_NAME"
model_provider = "openmodel"
```

If a `model` line already exists anywhere in the file, change that line rather than adding a second one.

Second, at the very bottom of the file, below everything already there:

```toml
[model_providers.openmodel]
name = "Hosted open model"
base_url = "YOUR_ENDPOINT"
env_key = "OPEN_MODEL_API_KEY"
wire_api = "responses"
```

Before saving, scroll the file once: every pre-existing line — `forced_login_method = "api"` included — must still sit above the `[model_providers.openmodel]` header. Line by line: `model` names what to ask for, `model_provider` routes requests through the `openmodel` entry, `base_url` is where they go, and `env_key` names the environment variable that will hold the key — the key itself never goes in this file. `wire_api = "responses"` declares that the endpoint speaks the OpenAI Responses API, the only protocol the app supports; an endpoint offering only plain chat completions cannot be re-pointed this way. The id `openmodel` is yours to change, except that `openai`, `ollama`, and `lmstudio` are reserved for built-ins. If your pinned build's own configuration reference disagrees with any key name here, the build's docs win — check them before you fight an error.

## Swap the placeholders

`YOUR_ENDPOINT` and `YOUR_MODEL_NAME` are the same placeholders `AUP_ENDPOINT_TEMPLATE.md` carries; the pin posted this morning has the real values and the key. Paste the endpoint and model name into both places — this config and your AUP's endpoint block — so the policy and the config agree about what they govern. Then set the key in a terminal, matching the name to whatever your `env_key` line says:

```
setx OPEN_MODEL_API_KEY "paste-the-key-here"
```

`setx` only reaches programs started afterward, so fully quit the app — not just its window — and reopen it. The restart is also what makes it re-read the config file. The key stays out of the config, out of the AUP, and out of anything git tracks.

## Verify which model answered

Send one smoke request — a small task your AUP allows — and check two things. First, the app should display `YOUR_MODEL_NAME` as the active model (the model picker or status line, wherever your pinned build shows it); if only the home models appear, the config never loaded. Second, the request should come back answered rather than erroring. Don't lean on asking the model what it is — models routinely answer that question with a name from their training data, so it proves nothing. The displayed model plus the `model_provider` line is the real proof: with that line set, requests have exactly one place to go.

## Roll back after the block

Restore the exact configuration you backed up before the re-point:

```powershell
Copy-Item "$env:USERPROFILE\.codex\config.toml.p8-backup" "$env:USERPROFILE\.codex\config.toml" -Force
```

Fully quit and reopen the app. Select `gpt-5.6-terra`; seeing it in the picker and as the active model confirms that the Terra pin and API-key sign-in are both restored. Do not try to roll back by commenting the current `model` line: that line replaced the Terra line during the re-point, so commenting it would leave future chats on an unpinned default. The environment variable can stay or go; remove it in Windows' Environment Variables dialog once the key it names is retired.

## When it doesn't work

- **Every request errors in a way that looks like a login problem.** A capped or mispasted key produces exactly this. Re-check the pin values character by character — endpoint, model name, key — and confirm the variable name matches `env_key` exactly. Then escalate with the exact error text, not a paraphrase.
- **Requests go nowhere and the config still says `YOUR_ENDPOINT`.** The placeholder never got swapped. Search the file for `YOUR_` and replace whatever you find.
- **The new model never appears in the app.** Either the app was not fully restarted, or the edit landed in a project-level `.codex\config.toml`, where provider lines are ignored. Confirm the path is `%USERPROFILE%\.codex\config.toml`, then restart again.
- **The key is set but not seen.** The variable was created after the app launched, or its name and `env_key` disagree by one character. Fix the name, quit completely, reopen.
- **A stray click bounces the app to a ChatGPT login after the re-point.** The provider table got pasted above the file's existing lines, so `forced_login_method = "api"` was swallowed into the table and stopped being a root key — it still reads fine in the file, which is what makes this one sneaky. Move the `[model_providers.openmodel]` block to the very bottom of the file, keep only the two `model` lines at the top, save, and fully restart the app.
