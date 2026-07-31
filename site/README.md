# Course site

**Canonical learner surface** for the AI Harness Bootcamp.

This bootcamp is **not a series of decks**. Exercises, pre-work, instruments, operator rituals, and references are published here for students and for the lead’s live operate-along.

## Look and feel

Follow **`VISUAL_SYSTEM.md`** and **`tokens.css`**.

| Reference | Role |
|---|---|
| [starzl.com](https://starzl.com) | Brand altitude, restraint, defense-industrial composure |
| Starzl quote + invoice PDFs | Paper document system: red disc mark, tracked labels, hairlines, meta grids, tables |

**Default:** paper/light courseware (PDF system) for readable exercises.  
**Sparse:** dark field surface for heroes, figures, operate-along canvases.

**Learner voice:** warm **guide-beside** — complete explanations, plain language, concepts defined when needed. Looks like Starzl; reads like someone beside you at the keyboard. See `VISUAL_SYSTEM.md` (voice section) and `MEMORY.md`.

## Intent

| Audience | Use |
|---|---|
| Students | Navigate the week, open block pages, launch kits, copy operator templates |
| Lead | Same pages on shared screen while operating and going deep with the AI |
| Builders | Repo markdown → site pages; tokens enforce Starzl visual law |

## Status

- Visual system documented  
- CSS tokens stubbed  
- App/framework not chosen yet — content still in repo markdown (`prework/`, `operator/`, `instruments/`, etc.)

## Do not

- Rebuild as slide decks with the site as an afterthought  
- Consumer edtech chrome (pastel, mascots, gamified confetti)  
- Cold expert walls or hype slogans on learner pages — use guide-beside prose  
- Hide teacher-only truth students need to operate  
- Long prose on pure black field backgrounds  


## Run locally

From the repo root:

```bash
python3 -m http.server 8080
```

Open [http://localhost:8080/site/](http://localhost:8080/site/)

Or open `site/index.html` directly (some browsers restrict fetch on sample viewer file://).

## Hosted (Railway)

Password-gated host at repo root: `server.py`. Configure `SITE_PASSWORD` (and optional `SITE_SECRET`). Full steps: [`HOSTING.md`](../HOSTING.md).
