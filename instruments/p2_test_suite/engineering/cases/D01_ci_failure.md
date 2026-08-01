# D01 — CI failure triage

## Input

```
[CI] pr-1842 · branch feature/retry-queue
✓ lint
✓ unit
✗ integration (12.4s)
  Error: Timeout waiting for redis at redis://cache:6379
  retry 3/3 failed
  at waitForRedis (tests/integration/queue.test.ts:88)
✗ pipeline failed

Also in log (noise):
  npm WARN deprecated uuid@3.4.0
  browserlist data 4 months old
```

## Task

In ≤8 bullets: what failed, most likely cause, what to check next, what is probably unrelated noise.
