# Resource figure specifications

Resource figures are deterministic SVG plates in the course's existing paper/red/gold family. Edit the JSON specification; `node scripts/build-resources.mjs` writes the SVG.

Every specification has:

```json
{
  "schemaVersion": 1,
  "resourceId": "P1-2",
  "figures": []
}
```

Normal handouts use exactly three roles: `orientation`, `mechanism`, and `diagnostic`. PC-1 uses one `compact` figure. Every figure requires `id`, `role`, `template`, `title`, `desc`, `caption`, `transcript`, and `eyebrow`.

Supported layouts:

- `flow`: `items`, each with `label` and `detail`; best for three to five ordered states.
- `comparison`: two to four `items`; best for exact distinctions or before/after patterns.
- `stack`: two to five `items`; best for layers, responsibility, or nested controls.
- `fork`: one `root` or `source` plus two to six `items`; best for branching explanations or decision paths.
- `timeline`: two to six `items`; best for state change, escalation, or evidence accumulation.
- `matrix`: `columns` plus `rows`; best for repeated-field comparison or predict-before-test drills.

The renderer supports short labels, not paragraphs. Put the complete relationship in `transcript`, use `caption` to tell the learner what to inspect, and keep essential meaning available without color.
