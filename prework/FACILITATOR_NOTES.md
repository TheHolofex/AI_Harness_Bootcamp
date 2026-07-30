# Pre-work — facilitator notes

## Design choice

**No golden image.** Students install and configure their own vanilla Windows workstation as a **pre-work module** before contact hours.

Why:

- Operators own the chair at work; install is part of literacy
- Avoids "lab magic" that won't transfer
- Moves install pain out of Monday mastery time without removing the experience

## Staff actions required BEFORE the pre-work window opens

The course now runs entirely on API keys. These are staff jobs, and every one of them blocks students if it slips.

### 1. Provision keys — one per student, per provider

Three providers: OpenAI, xAI, Anthropic. **One key per student, never a shared cohort key** — a shared key can't be revoked for one person, gives no per-student usage attribution, and turns one leak into twenty.

Wrap each key in the provider's isolation unit so a cap and a kill switch exist per student:

| Provider | Isolation unit | Console | Prefix |
|---|---|---|---|
| OpenAI | Project | platform.openai.com | `sk-proj-` |
| xAI | Team + per-key ACLs | console.x.ai | `xai-` |
| Anthropic | Workspace | platform.claude.com | `sk-ant-api03-` |

**Fund every account before day one.** All three are prepaid; none will serve a coding model at a zero balance, and the failure surfaces as an authentication-looking error rather than a bill.

**Set hard spend limits, not alerts.** On OpenAI the distinction is explicit: an alert notifies and lets traffic continue, a hard limit returns `429`. An alert alone will not stop a runaway agent loop.

**xAI keys are deny-by-default.** A freshly minted `xai-` key has access to nothing until you attach ACLs (`api-key:model:…`, `api-key:endpoint:chat`). A key that looks valid and does nothing will strand the whole OpenCode section — verify one end to end before issuing.

Budget roughly $100 per student per provider for a week of heavy agent use, and set the caps there. That leaves headroom for a bad loop without leaving the door open.

### 2. Pin versions and models, then post them

Students are told to use the cohort pin rather than latest. Post in the pre-work channel:

- **OpenCode version.** This one matters most. OpenCode ships fast and Windows support has regressed between releases — file-writing tools failing on Windows has been a live issue. Install a candidate on one machine, run the write proof, and pin what passes.
- **Model ids** for OpenAI and xAI. Do not let handouts carry hardcoded model names; providers rotate them. Confirm current ids the week the course runs.

### 3. Revocation plan

Anthropic is cleanest — archiving a workspace revokes all its keys at once. OpenAI is per-project. xAI is per-key, and note that **removing a user from the team does not revoke their keys**.

## What staff provides

- Three API keys per student, funded, capped, and ACL'd, in time for the pre-work window
- Pinned OpenCode version and model ids in the pre-work channel
- This pre-work pack + support channel hours
- Optional live "install clinic" (office hours), not a silent image drop
- Monday Block 0 **verification** protocol — not mass imaging

## What staff does not do

- Hand out a pre-baked golden laptop image as the default path
- Burn Block 0 AM re-teaching winget from zero for students who skipped pre-work
- Lower First Light mastery bars because pre-work was ignored

## Escalations that cannot be fixed from the student's seat

Triage these first when someone reports being stuck; no amount of retrying helps.

| Symptom | Reality |
|---|---|
| `Get-ExecutionPolicy -List` shows MachinePolicy or UserPolicy set | Group Policy overrides the student. IT ticket. |
| `$env:PROCESSOR_ARCHITECTURE` returns ARM64 | OpenCode won't start; goose has no ARM build. Different machine required. |
| No admin rights for elevation prompts | Git, Node, and Codex sandbox setup all need one. IT ticket. |
| Key returns 429 / insufficient quota | Cap or balance. Staff console fix. |
| xAI key authenticates but reaches no model | Missing ACLs on the key. Staff console fix. |

## Monday gate

1. Spot-check health check GREEN/YELLOW at the door or in the first 20 minutes.
2. RED goes to the rescue table on a parallel track; do not stall First Light for the cohort.
3. B0 MVP still requires four-tool write proof — pre-work should already have produced it; class confirms and proceeds to the instrument.

Ask for the two version details the health check collects: **OpenCode version** and **Codex sandbox mode**. Those are what differ between machines when something behaves oddly mid-block.

## Rescue

- YELLOW with a documented workaround: allow into First Light.
- RED that is keys-only: staff can usually unblock faster than install-from-zero.
- RED "never started": evening make-up; not a redesign of the school into an image depot.

## Contact-week lead posture (reminder)

Lead runs missions live on screen with talk-through and real-time AI depth. Pre-work stays student-owned — Monday is verify plus First Light operate-along, not an install lecture.
