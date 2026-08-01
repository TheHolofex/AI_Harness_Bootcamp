# Start here

## Run the course site

Local (no password), from repo root:

```bash
cd /path/to/AI_Harness_Bootcamp
python3 -m http.server 8080
```

Open http://localhost:8080/site/

Password-gated (local or Railway) — set `SITE_PASSWORD` and run:

```bash
export SITE_PASSWORD='your-cohort-password'
python3 server.py
```

Staff who also want the keys served add a second, different password:

```bash
export SITE_PASSWORD='your-cohort-password'
export STAFF_PASSWORD='a-different-password-students-never-see'
python3 server.py
```

Open http://localhost:8080/site/ (login first). Deploy notes: `HOSTING.md`.

## Map

| Path | What |
|---|---|
| `site/` | Learner + lead web course |
| `prework/` | Student-owned Windows install |
| `operator/` | Brief, log, bars, adversarial, measure, transfer |
| `instruments/` | P2/P3/P8 shared kits (eng + mission_ops) |
| `mission_flesh/` | Corpora and packs for each block |
| `lead/` | Operate-along helpers |
| `diagrams/` | Circuit / pulse / equations |
| `staff/` | Answer keys and the pin sheet. Not in the clone — see below |

## Overnight build note

This snapshot is teachable end-to-end for iterate-to-final. Placeholders remain for live seats and `YOUR_ENDPOINT`.


## Interactive checklists

http://localhost:8080/site/checklists/

Each block (B0–P8) has a full step-by-step checklist with checkboxes. Progress uses browser localStorage.


## Pre-work

- Install + verify as you go: http://localhost:8080/site/checklists/prework-install.html
- Hub: http://localhost:8080/site/prework.html
- Monday clinic + First Light: http://localhost:8080/site/blocks/b0.html
- Monday morning, students open this repo's root folder as their Codex app project for the week (cloned in `prework/INSTALL_GUIDE.md` section 13) — not the smoke folder
- Optional rescue re-test only: `prework/HEALTH_CHECK.md`

## Staff (before pre-work window)

- Pin sheet: `staff/lead/COHORT_PIN.md`
- Rotting facts (any machine): `python3 .github/scripts/verify-stack-facts.py`
- Windows install smoke: `powershell -ExecutionPolicy Bypass -File .github\scripts\prework-verify.ps1`
- Facilitator notes: `prework/FACILITATOR_NOTES.md`
- Hosted site: `HOSTING.md` — Railway + `SITE_PASSWORD`

### The `staff/` directory

Answer keys, facilitator keys, and the pin sheet are **not in this repository**. They
were removed from it deliberately: students clone this tree, and anything in it is
readable by every student and by every model they point at a folder.

Get `staff/` from the course lead over the channel you use for keys and passwords, and
unpack it at the repo root so the paths read `staff/lead/COHORT_PIN.md`,
`staff/mission_flesh/p5/FACILITATOR_KEY.md`, and so on. `.gitignore` already excludes it,
so it cannot be committed back by accident. Full contents and placement:
`staff/README.md`.

To reach the same files on the hosted site, set `STAFF_PASSWORD` to something other than
`SITE_PASSWORD` and sign in with it. The cohort password does not open `staff/`.
