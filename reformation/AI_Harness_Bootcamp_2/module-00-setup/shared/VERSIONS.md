# Course setup pins

Checked: 2026-08-12 · nvm installer tag recorded here on 2026-08-14

These are course compatibility pins, not a promise that the newest release is always better.

| Component | Course value | Why |
|---|---:|---|
| Node.js | 24.x | Satisfies the repository's strictest declared engine, `>=22.22 <25`, and n8n's current requirement. No path pins an exact patch release: each platform installs Node 24 with its own package manager, and the setup check reads the running major version and the absolute path it resolved to. |
| Python | 3.12+ | Matches the deployed repository runtime floor and current course scripts |
| OpenCode | 1.18.17 | Current npm stable checked on 2026-08-12; all paths install the same build |
| n8n | 2.34.5 | Current npm stable checked on 2026-08-12; requires Node `>=22.22` |
| nvm | 0.40.6 | The Ubuntu and WSL paths download `install.sh` from the `v0.40.6` tag, so both learners read and run the same installer text. A moving tag would change the script between the reading step and the running step. |
| Codex CLI | Current official stable | Vendor standalone installer or `@openai/codex`; installed version is recorded |
| goose CLI | `stable` release channel | Official AAIF installer; installed version is recorded because `stable` moves |
| Git | Current supported package-manager release | Functional clone/revision checks decide readiness |
| Obsidian | Current official stable | GUI install is platform-specific; the observed file list in the vault decides readiness |

## Source checks

```text
npm view opencode-ai version
npm view n8n version engines
npm view @openai/codex version engines
git ls-remote --tags https://github.com/nvm-sh/nvm v0.40.6
```

The strict repository engine declarations are in:

- `instruments/osint_desk/package.json`
- `instruments/p3_evidence_surface/package.json`
- `mission_flesh/pi/package.json`

## Update rule

Every version literal that any platform path hard-codes appears in the table above. A guide that names a version this file does not carry is drift, whether or not it installs.

Change a pin only when all five platform paths can install it and the shared verifier still passes. Record the date, source, old value, new value, and compatibility evidence. Never let one platform drift silently.
