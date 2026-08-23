# Module 0 · Give AI a clear, limited job

One AI command-line tool drafts a short email from a supplied set of facts. You check the draft against the source yourself, prove your own check is capable of failing, change one supplied fact and rerun, then decide whether anyone may read the result.

The case is fictional. Your draft stays with named course participants. Do not publish it, send it to a real operations list, or present it as a public movement order.

`HOLD` is a result you are allowed to record. It means you stopped and wrote down why, instead of producing something you cannot stand behind. If a tool or a file you need is missing, write `HOLD`, save the exact error text, and ask for help. Do not spend your working time rebuilding your machine.

## Timebox

| Work | Time |
|---|---:|
| Work folder, and the control that decides acceptance | 10 minutes |
| The case and the practice checker, read in full | 10 minutes |
| Delegation split and responsibility screen | 10 minutes |
| Frozen direction brief | 10 minutes |
| First draft and the practice check on it | 15 minutes |
| One material claim traced to the source | 15 minutes |
| Falsifier run against a deliberately wrong copy | 10 minutes |
| Capability-limit statement | 10 minutes |
| Sharing decision | 5 minutes |
| Changed input applied and the difference compared | 20 minutes |
| Handoff | 5 minutes |

Your first checked draft must exist within 60 minutes of starting.

## 1. Set up the work folder

Everything you produce goes in one folder outside the course repository, so that your work and the course files never get confused with each other.

Create a folder named `module-00-work` in your home folder.

**Windows PowerShell — normal user. No administrator rights are needed.**

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\module-00-work" | Out-Null
Set-Location "$env:USERPROFILE\module-00-work"
Get-Location
```

**macOS Terminal, Ubuntu, Arch Linux, or Ubuntu on WSL — normal user.**

```bash
mkdir -p "$HOME/module-00-work"
cd "$HOME/module-00-work"
pwd
```

The last line prints the folder you are now working in. The first part is your own home folder, so yours will read something like one of these:

```text
C:\Users\yourname\module-00-work
/Users/yourname/module-00-work
/home/yourname/module-00-work
```

Every command in the rest of this lab runs in that folder. If you open a new terminal later, move back into it first with the `Set-Location` or `cd` line above.

Copy the source packet, request, changed input, and practice checker into the folder. The originals stay where they are and stay unchanged.

**Windows PowerShell — normal user.**

```powershell
Set-Location "$env:USERPROFILE\module-00-work"
$casedir = Join-Path $env:USERPROFILE 'course\AI_Harness_Bootcamp\reformation\AI_Harness_Bootcamp_2\module-00-setup\shared\case'
Copy-Item -Destination . -Path (Join-Path $casedir 'SOURCE_PACKET.md'), (Join-Path $casedir 'REQUEST.md'), (Join-Path $casedir 'CHANGED_INPUT.md'), (Join-Path $casedir 'check_artifact.py')
Get-ChildItem -Name
```

**macOS Terminal, Ubuntu, Arch Linux, or Ubuntu on WSL — normal user.**

```bash
cd "$HOME/module-00-work"
casedir="$HOME/course/AI_Harness_Bootcamp/reformation/AI_Harness_Bootcamp_2/module-00-setup/shared/case"
cp "$casedir/SOURCE_PACKET.md" "$casedir/REQUEST.md" "$casedir/CHANGED_INPUT.md" "$casedir/check_artifact.py" .
ls -1
```

You should see exactly these four names, in whatever order your system sorts them:

```text
CHANGED_INPUT.md
REQUEST.md
SOURCE_PACKET.md
check_artifact.py
```

If the copy reports that a path does not exist, your course repository is somewhere else. Find it, use its path in place of the one above, and write down the path you used.

The finished work is those four copies plus twelve files you write:

```text
module-00-work/
├── acceptance-control.md
├── direction-brief.md
├── minimum-screen.md
├── prompt.txt
├── artifact.md
├── source-check.md
├── falsifier-probe.md
├── capability-limit.md
├── decision.md
├── changed-input-prediction.md
├── artifact-changed.md
└── handoff.md
```

## 2. Confirm what decides acceptance

Find out what will judge your work before you produce any of it. Otherwise you are writing toward a standard you have only guessed at.

The checker you just copied is the practice check. You are meant to read it. Print its opening lines.

**Windows PowerShell — normal user.**

```powershell
Set-Location "$env:USERPROFILE\module-00-work"
Get-Content .\check_artifact.py -TotalCount 16
```

**macOS Terminal, Ubuntu, Arch Linux, or Ubuntu on WSL — normal user.**

```bash
cd "$HOME/module-00-work"
head -n 16 check_artifact.py
```

Among the lines it prints are these three:

```text
You are meant to read this file. It is not hidden from you, and editing it changes
nothing that decides your result -- the control that decides acceptance is held by
your evaluator and is not on this machine.
```

Your result is decided by a protected acceptance control that your evaluator runs and that is not on this machine. You cannot read it or change it, and editing the practice checker in front of you moves nothing. The standard that control applies is the published rubric, which you can read in full before you start.

Write `acceptance-control.md`:

```markdown
# Protected acceptance control

Checkers present on this machine (file names):
What the practice checker's own header says decides acceptance:
Where the protected acceptance control runs, and who runs it:
Published standard it applies, and where I read it:
What changes for my result if I edit the practice checker:
Two qualities of a draft the practice checker cannot judge:
```

Leave the last line until you have read the checker in the next step.

## 3. Read the case and the practice checker

Open these files in your work folder:

- `SOURCE_PACKET.md` — the only facts you may use
- `REQUEST.md` — what the email must do
- `CHANGED_INPUT.md` — do not open this one yet
- `check_artifact.py` — the practice check, in full

Read the checker's body, not only its header. It looks for a set of visible, mechanical things: a subject line, a word count, particular facts stated rather than denied, and services the source does not confirm.

Then notice what it cannot decide: whether the email is clear, whether an unsupported promise would harm the reader, whether the audience is right, and whether the draft should be used at all.

Now fill in the last line of `acceptance-control.md` with two of those qualities. Anything you write there is a quality nobody and nothing on your machine will check for you.

## 4. Choose what AI should and should not do

Start `direction-brief.md` with this section:

```markdown
## Delegation decision

AI may:

Human judgment stays with me for:

AI must not:

Why this split fits the case:
```

A sound split lets AI draft and reorganize the supplied facts. You still decide what the source means, whether the email meets the request, and whether anyone may use it. If you choose a different split, name who makes each of those three decisions.

**Write `HOLD` if:** the task would require the model to invent missing services, decide real dispatch policy, or contact real depot personnel.

## 5. Complete the minimum responsibility screen

Answer these questions before you generate anything, because two of them can end the work. Write `minimum-screen.md`:

```markdown
# Minimum responsibility screen

Source and data authority:
Sensitive data in this case:
Affected audience or person:
Disclosure needed inside this exercise:
Real-world decision this draft cannot make:
Human decision owner:
Unresolved item:
Decision: PROCEED TO CLASS DRAFT / HOLD
```

For this case, use only the supplied source packet. The draft stays with named course participants, contains no personal data, and is never published. You make the final decision.

If any line is unresolved, write `HOLD`. Do not draft until you know the source may be used and who makes the final decision.

## 6. Freeze the direction brief

Pin down every part of the request that the model could otherwise satisfy in several incompatible ways. Complete the rest of `direction-brief.md` and save it before you run anything:

```markdown
# Direction brief

Audience:
Draft and where classmates will read it:
Outcome:
Allowed sources:

## Material constraints

1.
2.
3.

Precedence when instructions conflict:
Acceptance condition:
Plausible falsifier:
Prohibited result:
Stop condition:
Correction limit:
Decision owner:
```

Make each of these testable by someone who was not there:

- only the supplied source packet may establish facts;
- the draft is a 130–190 word email with a subject line and a contact line;
- unknown services stay unknown rather than becoming promises;
- no public or consequential use is allowed;
- the work stops if a material fact cannot be traced, or if a correction would change the mission.

For **Plausible falsifier**, do not write "the email is wrong." Write the specific observation that would show a named claim in your draft is wrong — for example, "a coordinator reading this email sends staff to a locked door." You will run it in step 9, so write one you can actually carry out.

For **Correction limit**, write two correction attempts, then `HOLD`.

If you find a problem in the brief later, keep this first version and record what you changed and why.

## 7. Produce the first draft

Point the tool at the frozen brief and the supplied files rather than restating the facts in the prompt, so the files stay the single source of the facts. Writing the instruction into a file also means you still have it afterwards, word for word.

In any text editor, save this as `prompt.txt` in your work folder:

```text
Read direction-brief.md, REQUEST.md, and SOURCE_PACKET.md. Follow the brief's source
and sharing limits. Draft the requested email and write it to artifact.md. Do not use
facts from outside the supplied files. After writing, report the path only.
```

Now run one of the AI command-line tools on your machine.

**macOS Terminal, Ubuntu, Arch Linux, or Ubuntu on WSL — normal user.**

```bash
cd "$HOME/module-00-work"
codex exec --sandbox workspace-write --skip-git-repo-check "$(cat prompt.txt)"
```

**Windows PowerShell — normal user.**

```powershell
Set-Location "$env:USERPROFILE\module-00-work"
codex exec --sandbox workspace-write --skip-git-repo-check (Get-Content .\prompt.txt -Raw)
```

If you set up `opencode` or `goose` instead, the equivalent calls are `opencode run -m xai/grok-4.5 "<instruction>"` and `goose run --no-session --provider xai --model grok-4.5 -t "<instruction>"`.

The tool's closing message is its own report of what it did. Ask the file system instead.

**Windows PowerShell — normal user.**

```powershell
Set-Location "$env:USERPROFILE\module-00-work"
Get-Item .\artifact.md | Format-List Name, Length, LastWriteTime
```

**macOS Terminal, Ubuntu, Arch Linux, or Ubuntu on WSL — normal user.**

```bash
cd "$HOME/module-00-work"
ls -l artifact.md
wc -w artifact.md
```

You should see a size of roughly 800 to 1,300 bytes for a 130–190 word email, a write time within the last few minutes, and a word count in that range. If the command instead reports that the file does not exist, the run failed, whatever the tool said. Record it as a failed operation. Do not create the missing file by hand and call the run successful.

Then open `artifact.md` in your editor and read it end to end before any check touches it.

The practice check runs on Python 3.12 or newer. Print the version of the interpreter you are about to use, and read the number it prints.

**Windows PowerShell — normal user.**

```powershell
Set-Location "$env:USERPROFILE\module-00-work"
python --version
```

**macOS Terminal — normal user.**

```bash
cd "$HOME/module-00-work"
python3.12 --version
```

**Ubuntu, Arch Linux, or Ubuntu on WSL — normal user.**

```bash
cd "$HOME/module-00-work"
python3 --version
```

You should see `Python 3.12.` followed by a patch number, or a higher version such as `Python 3.13.2`. If the number is 3.11 or lower, or the command is not found, this shell is not the one your setup path prepared: open a new terminal, move back to the work folder, and run it again. If it is still below 3.12, write `HOLD` and save the version line exactly as it printed.

The name that printed 3.12 or newer is the one you use for every check that follows. Run the check on your draft.

**Windows PowerShell — normal user.**

```powershell
Set-Location "$env:USERPROFILE\module-00-work"
python .\check_artifact.py .\artifact.md
```

**macOS Terminal — normal user.**

```bash
cd "$HOME/module-00-work"
python3.12 check_artifact.py artifact.md
```

**Ubuntu, Arch Linux, or Ubuntu on WSL — normal user.**

```bash
cd "$HOME/module-00-work"
python3 check_artifact.py artifact.md
```

Each requirement prints its own line. The last line you are looking for is:

```text
PASS: mechanical requirements passed; this is practice only
```

If instead the last line begins `HOLD:`, save the whole output before you touch anything. Ask the AI tool for one correction, then run the check again. Stop after two correction attempts. If it still fails, write `HOLD`, keep the saved output, and hand the failure and the output to your evaluator.

## 8. Check one material claim at the source

Choose the claim most likely to change what a reader does: hours, entrance, eligibility, or capacity. Open the source packet and compare it yourself. Do not ask the model that produced the claim whether the claim is supported.

Write `source-check.md`:

```markdown
# Source check

Claim in the draft:
Source location and exact supporting text:
Interpretation:
What would falsify the claim:
Result: PASS / HOLD
```

Then read every sentence of the draft for services the source does not confirm: meals, medical care, overnight shelter, chargers, childcare, or a shuttle. The source packet names those as unconfirmed, so a sentence that promises one has invented it.

## 9. Run your falsifier

Make the mistake on purpose and watch your check catch it. Until you have seen it fail once, you cannot tell whether it passed your draft because the draft is right or because it never looks at that claim.

Copy your draft, then edit the copy so that the one claim you checked in step 8 is stated wrongly — send readers to the Yard Street doors, or move the hours, or require identification, or change the capacity.

**Windows PowerShell — normal user.**

```powershell
Set-Location "$env:USERPROFILE\module-00-work"
Copy-Item .\artifact.md .\falsifier-probe.md
```

**macOS Terminal, Ubuntu, Arch Linux, or Ubuntu on WSL — normal user.**

```bash
cd "$HOME/module-00-work"
cp artifact.md falsifier-probe.md
```

Edit `falsifier-probe.md` — one claim, one sentence. Leave everything else alone.

Now run your falsifier against the probe. If your falsifier is a reading rather than a command — "open the probe and see which door it sends people to" — carry out that reading and write down the sentence you read. If it is something the practice checker already tests, run the checker:

**Windows PowerShell — normal user.**

```powershell
Set-Location "$env:USERPROFILE\module-00-work"
python .\check_artifact.py .\falsifier-probe.md
```

**macOS Terminal — normal user.**

```bash
cd "$HOME/module-00-work"
python3.12 check_artifact.py falsifier-probe.md
```

**Ubuntu, Arch Linux, or Ubuntu on WSL — normal user.**

```bash
cd "$HOME/module-00-work"
python3 check_artifact.py falsifier-probe.md
```

You should see one requirement fail and name the sentence or number it found. If you inverted the entrance, the line reads like this, with your own sentence at the end:

```text
FAIL: entrance — the draft denies it: Please use the Yard Street doors.
```

and the run ends:

```text
HOLD: 1 mechanical requirement(s) failed; this is practice only
```

Add this to the bottom of `source-check.md`:

```markdown
## Falsifier run

Claim I attacked:
Exact change I made in falsifier-probe.md:
Command I ran:
Observed failure, copied exactly:
Requirements that stayed PASS:
What this tells me the check can and cannot catch:
```

If nothing failed, your falsifier does not reach the claim you care about. That is worth more than a green result: it means the check would not have caught the same mistake in your real draft either. Say so in the record, and say which claims are therefore unverified.

Keep `falsifier-probe.md`. Do not use it as your draft, and do not let any later step overwrite `artifact.md` with it.

## 10. Write the capability-limit statement

Four different things acted in the run you just did, and they fail in different ways. Separating them is how you know what to fix when something goes wrong, and what you can rely on next time.

Write `capability-limit.md` from what you saw in your own run — not from what you have read about these tools:

```markdown
# Capability and limit

What the model output produced:
What the product around it did (the command-line tool, its sandbox, its file writing):
What the harness controlled (the direction brief, the checks, the work folder):
What stayed a human decision:

One capability observed in this run:
One limitation observed in this run:
```

Both of the last two lines must name something you watched happen in this run. Instead of "it can summarize well", write what you saw: "it reorganized eleven confirmed facts into a 164-word email in one pass, with no fact from outside the packet." For the limitation, instead of "it sometimes hallucinates", write "it wrote that chargers were available, which the packet lists as unconfirmed, and the practice check caught it."

## 11. Decide whether classmates may review the draft

Write `decision.md`:

```markdown
# Decision

Practice-check result, last line of the output copied exactly:
Material source-check result, and the source text it rests on:
Falsifier-run result, failure line copied exactly:
Minimum-screen result, and any item still open:
Known limitation:
Residual risk:
Decision owner:
Decision: PASS FOR CLASS REVIEW / HOLD
Reason:
```

`PASS FOR CLASS REVIEW` means only named course participants may read the draft. It cannot be published or used to direct real depot operations.

Choose `HOLD` if a claim that affects the reader has no source, a responsibility question is still open, two corrections have failed, a file is missing, or a real official would have to approve the result.

## 12. Apply the changed input

Open `CHANGED_INPUT.md` now. Before you run anything, write `changed-input-prediction.md`:

```markdown
# Changed-input prediction

Material statements that must change:
Material statements that must not change:
Checks to rerun:
Unexpected change that would cause HOLD:
```

The capacity changes from 60 to 45. Days, hours, address, entrance, eligibility, services, and the contact line do not change.

Ask the AI tool to write `artifact-changed.md` from the original draft and the changed input. Name the new file in the instruction so it cannot overwrite `artifact.md`.

Run the practice check against the changed draft, using the same command name that printed 3.12 or newer in step 7 and naming `artifact-changed.md` in place of `artifact.md`. The checker expects capacity 60, so a correct revision to 45 makes it fail that one requirement:

```text
FAIL: capacity 60 — the draft attaches [45] to capacity, not 60
```

That failure is correct. The checker still describes the original case. Do not edit it to make the failure go away — a check you edit to fit the answer stops being a check.

Now look at the difference yourself:

**Windows PowerShell — normal user.**

```powershell
Set-Location "$env:USERPROFILE\module-00-work"
Compare-Object (Get-Content .\artifact.md) (Get-Content .\artifact-changed.md)
```

**macOS Terminal, Ubuntu, Arch Linux, or Ubuntu on WSL — normal user.**

```bash
cd "$HOME/module-00-work"
diff -u artifact.md artifact-changed.md
```

Record whether the capacity moved from 60 to 45 as you predicted, and record every other change the comparison shows, including any that would change what a reader does.

## 13. Write the handoff

Write `handoff.md`:

```markdown
# Module 0 handoff

Purpose and audience:
Sources used and excluded:
Current decision:
How to run the visible practice check:
Strongest evidence:
Known limitation:
Stop condition:
Falsifier and what it caught:
Changed-input result:
What the next owner should inspect first:
```

Someone else should be able to find the draft, its source, the check results, your decision, and the known limit without asking you where anything is.

## Completion check

You are done when:

- the four copied case files and the twelve files you write are all in `module-00-work`;
- `acceptance-control.md` records that the deciding control is off this machine and names the standard it applies;
- the first checked draft appeared within 60 minutes, or the record says why it did not;
- the delegation decision, minimum screen, and direction brief were saved before the first AI run;
- the material claim is traced to exact supplied source text;
- your falsifier ran against `falsifier-probe.md` and `source-check.md` records the observed failure;
- `capability-limit.md` separates model output, product surface, harness control, and human decision, and names one capability and one limitation you watched happen;
- no more than two correction attempts were made, and the first failed output is preserved;
- the decision is `PASS FOR CLASS REVIEW` or `HOLD`;
- the changed-input prediction was written before the second run, `artifact.md` is unchanged, and the delta is the one you predicted; and
- the handoff names the limitation and the first thing to inspect.

Keep the work folder where you made it, so the next person to look at this work finds every file in one place. Keep it out of the shared repository: nothing you produced here belongs in the clone.
