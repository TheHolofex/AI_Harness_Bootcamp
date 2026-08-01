# AI Harness Bootcamp

A five-day course in **operating** AI coding agents, rather than using them.

That distinction is the whole design. Most people arrive able to get useful output from a chat
window, and stop there — fluent at prompting, with no way to tell a good result from a confident
one. The week is built to produce something else: an operator who can stand up their own
workstation, decide what a machine is allowed to touch before handing it work, put two engines on
the same problem and own the verdict, and tell the difference between a claim and evidence on disk.

The arc runs **direct → harness → verify → adjudicate → bound → choose machine → transfer**, one
capability per block, B0 through P8.

## What the week is trying to leave behind

Four commitments shape almost every decision in this repository.

**You own the chair the machine sits in.** There is no golden image and no finished laptop handed
over. Students install the whole stack themselves, on their own hardware, against their own keys.
Owning that pain once is cheaper than never owning it — and it means a tool breaking on Wednesday
is a thing they can reason about instead of a thing that happened to them.

**Evidence, not claims.** A tool saying it wrote the file is a claim; the file in Explorer is
evidence. Every block ends against written pass bars, and every verdict goes through an adversarial
review whose job is to attack it. "It ran" is never a pass.

**One mind agrees with you too easily.** The comparator work runs the same frozen brief through two
genuinely different engines, then asks the student to adjudicate — not to average. Keeping those
engines independent is a real piece of setup, not a formality, and the course treats it that way.

**It has to survive Monday.** The goal is not a good week. It is someone who still runs this loop
at their own desk once the scaffolding is gone, which is why transfer is a thread through every
half-day rather than a Friday worksheet.

## Getting oriented

Students start at **[`prework/README.md`](prework/README.md)** and finish before Monday — it stands
up the workstation and takes a focused evening or two.

Staff start at **[`START_HERE.md`](START_HERE.md)** for run modes, the repo map, and what has to be
true before the pre-work window opens.

The course itself is a website, served from this repository.

| Path | What |
|---|---|
| `site/` | The course — block pages, checklists, references |
| `prework/` | Student-owned Windows install |
| `operator/` | Brief, log, pass bars, adversarial review, measurement, transfer |
| `instruments/` | Shared kits for the comparator and scoring blocks |
| `mission_flesh/` | Corpora and packs per block |
| `lead/` | Facilitator material |
| `server.py` | Password-gated host for deploying the site — see `HOSTING.md` |

Facilitator material ships alongside the course material here, and `server.py` keeps it off the
hosted site. A clone is not a sealed copy, though — during the week, the line between what you work
out for yourself and what has already been worked out is one you hold, not one the repository holds
for you.
