# Pre-work section diagrams

Crisp, script-free SVG diagrams for the AI Harness Bootcamp install and health-check pages. All diagrams use the paper-surface Starzl visual system, selectable text, and an internal `<title>` for standalone accessibility.

## Asset index

| File | Placement |
|---|---|
| `install-overview.svg` | Install journey overview for the pre-work hub |
| `install-before-you-begin.svg` | Before you begin |
| `install-00-baseline.svg` | 0 · Baseline machine |
| `install-01-terminal.svg` | 1 · Terminal and PowerShell |
| `install-02-winget.svg` | 2 · winget, the package manager |
| `install-03-git.svg` | 3 · Git for Windows |
| `install-04-runtime.svg` | 4 · Node.js and Python |
| `install-05-keys.svg` | 5 · Your three API keys |
| `install-06-smoke.svg` | 6 · Your smoke folder |
| `install-07-codex.svg` | 7 · Codex — your home for the week |
| `install-08-opencode.svg` | 8 · OpenCode — your second engine |
| `install-09-pi.svg` | 9 · Pi — the bare loop |
| `install-10-goose.svg` | 10 · goose — bounded, repeatable work |
| `install-11-obsidian.svg` | 11 · Obsidian |
| `install-12-n8n.svg` | 12 · n8n |
| `install-13-repo.svg` | 13 · Course repo and operator pack |
| `install-14-claude-optional.svg` | 14 · Claude Code — optional third engine |
| `install-15-health-gate.svg` | 15 · Health check gate |
| `install-when-something-breaks.svg` | When something breaks |
| `health-overview.svg` | Health-gate journey overview |
| `health-how-to-run.svg` | How to run this gate |
| `health-a-foundations.svg` | A · Foundations |
| `health-b-keys.svg` | B · Your three keys |
| `health-c-agents.svg` | C · Four required agents — files on disk |
| `health-d-support.svg` | D · Supporting tools |
| `health-e-ready.svg` | E · Operator readiness |
| `health-result.svg` | Gate result |

## Usage

Place the matching figure immediately after its section `<h2>`:

```html
<figure class="section-diagram">
  <img src="../assets/prework/install-03-git.svg" alt="Diagram: 3 · Git for Windows — place in pre-work journey" width="1120" height="220" loading="lazy" decoding="async" />
</figure>
```

Use `install-overview.svg` at 1120 × 280 and `health-overview.svg` at 1120 × 240. Section diagrams are 1120 × 220. Keep the surrounding figure border in CSS; the SVGs deliberately carry no outer border so they remain reusable in print and other paper surfaces.

Claude Code is encoded with the gold optional treatment. Completed stages use a crimson disc; the current stage uses a filled crimson capsule. The repair diagram is intentionally marked “ANY STAGE” because recovery is cross-cutting rather than a numbered install stage.
