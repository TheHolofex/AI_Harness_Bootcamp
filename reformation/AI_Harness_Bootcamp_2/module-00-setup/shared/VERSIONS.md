# Required tool identities

Use the exact OMP release and provider/model pair below. A newer executable or a similarly named model is not an automatic substitute.

| Component | Required value | Check |
|---|---|---|
| Oh My Pi | 18.3.5 | The verified executable reports `omp/18.3.5`. |
| Provider/model | `openrouter/anthropic/claude-sonnet-4.6` | The launcher and actual run receipts agree on OpenRouter and Sonnet 4.6. |
| Credential | `OPENROUTER_API_KEY` | A presence-only check reports `SET` in the process that launches OMP. |
| Python | 3.12 or newer | Resolve its absolute executable path and inspect its version. |
| Git | A supported release for your operating system | Git runs and the intended checkout is readable. |
| Browser and text editor | An accessible combination you can operate | You can read instructions, edit plain-text work files, and inspect actual outputs. |

Download the OMP binary and `SHA256SUMS.txt` from the [same v18.3.5 release](https://github.com/can1357/oh-my-pi/releases/tag/v18.3.5). Select the asset for the operating system in which it will run:

| Runtime | ARM64 asset | x86-64 asset |
|---|---|---|
| macOS | `omp-darwin-arm64` | `omp-darwin-x64` |
| Linux, including Ubuntu in WSL | `omp-linux-arm64` | `omp-linux-x64` |
| Native Windows | `omp-windows-arm64.exe` | `omp-windows-x64.exe` |

Verify the selected file's checksum before installation or first execution. The Unix user destination is `~/.local/bin/omp`; native Windows uses `%LOCALAPPDATA%\omp\omp.exe`. Preserve a different existing installation rather than overwrite it silently.

The launcher isolates runtime configuration, exposes only declared course tools, and disables automatic retries, model fallback, cache warming, unrelated extensions, skills, and persistent sessions. Use that launcher for exercises rather than a personal OMP profile. A setup check alone does not prove these controls acted during a model turn; inspect the run's receipts.

No other model-provider key, vendor login, agent CLI, note-taking application, or workflow service is required. If the pinned release or model is unavailable, retain the failure and hold that lane. Do not choose an unreviewed substitute to obtain a passing label.
