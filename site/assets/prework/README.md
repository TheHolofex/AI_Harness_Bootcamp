# Pre-work section diagrams

Crisp, script-free SVG diagrams for the AI Harness Bootcamp install pages. All diagrams use the paper-surface Starzl visual system, selectable text, and an internal `<title>` for standalone accessibility.

## Asset index

| File | Placement |
|---|---|
| `install-overview.svg` | Install journey overview for the pre-work hub |
| `install-before-you-begin.svg` | Install pre-work: Before you begin |
| `install-00-baseline.svg` | Install pre-work: 0 · Baseline machine |
| `install-01-terminal.svg` | Install pre-work: 1 · Terminal and PowerShell |
| `install-02-installers.svg` | Install pre-work: 2 · Download the core installers |
| `install-03-git.svg` | Install pre-work: 3 · Git and the course repo |
| `install-04-runtime.svg` | Install pre-work: 4 · Node.js and Python |
| `install-05-keys.svg` | Install pre-work: 5 · Your three API keys |
| `install-06-smoke.svg` | Install pre-work: 6 · Your smoke folder |
| `install-07-codex.svg` | Install pre-work: 7 · Codex — your home for the week |
| `install-08-opencode.svg` | Install pre-work: 8 · OpenCode — your second engine |
| `install-09-pi.svg` | Install pre-work: 9 · Pi — the bare loop |
| `install-10-goose.svg` | Install pre-work: 10 · goose — recipe, tools, mode, schedule |
| `install-11-obsidian.svg` | Install pre-work: 11 · Obsidian |
| `install-12-n8n.svg` | Install pre-work: 12 · n8n |
| `install-13-repo.svg` | Install pre-work: 13 · Open and check the course files |
| `install-14-claude-optional.svg` | Install pre-work: 14 · Claude Code — optional third engine |
| `install-when-something-breaks.svg` | Install pre-work: When something breaks |

## Usage

Place the matching figure immediately after its section `<h2>`:

```html
<figure class="section-diagram">
  <img src="../assets/prework/install-03-git.svg" alt="Diagram: 3 · Git for Windows — place in pre-work journey" width="1120" height="220" loading="lazy" decoding="async" />
</figure>
```

Use `install-overview.svg` at 1120 × 280. Section diagrams are 1120 × 220. Keep the surrounding figure border in CSS; the SVGs deliberately carry no outer border so they remain reusable in print and other paper surfaces.

Claude Code is encoded with the gold optional treatment. Completed stages use a crimson disc; the current stage uses a filled crimson capsule. The repair diagram is intentionally marked “ANY STAGE” because recovery is cross-cutting rather than a numbered install stage.
