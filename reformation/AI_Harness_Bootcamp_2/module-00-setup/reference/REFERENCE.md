# Reference: Module 0 and the initial course setup

**Version:** 2 · **Frozen on:** 2026-08-14 · supersedes v1 (2026-08-12)
**Scope:** Module 0 learner material, shared setup contract, five platform setup paths, and the acceptance machinery that decides them
**Supported paths:** Windows PowerShell only, Windows with WSL 2 and Ubuntu, macOS, Ubuntu, Arch Linux
**Artifact type:** procedural learner material plus the executable checks that grade it. "Acceptance oracle" here means executable tests plus a named human judge with a written rubric; "test-driven" means the checks are written and observed failing before the material they govern; "performant" means time-to-first-checked-artifact and learner failure rate, both measured, never estimated.
**Changes from v1 are recorded in `AMENDMENTS.md`.** v1's self-contradictions on headless Ubuntu and on the session budget are resolved here rather than inherited.

---

## 1. The need, stated precisely

A capable professional arrives with the laptop they will use for the course. Its shell, runtimes, course files, credentials, and AI tools may be missing, stale, split across two environments, or working only in the one warm terminal where they were installed. They need one path that takes that machine to a visible, restartable state, and then uses it to complete a first bounded AI-assisted task whose acceptance they cannot quietly move.

This prevents five failures:

1. an installer reports success but the command cannot be found in a new shell;
2. a key works once because it was pasted where it will persist, or exposed in history;
3. Windows and WSL tools or files mix until neither environment is reproducible;
4. an AI tool reports it wrote a file when no acceptable file exists;
5. setup consumes the session and produces no evidence the learner can do the work.

**Done:** after following exactly one platform path, the learner opens a fresh shell, runs the course check, proves the required tools and repository work in that process, loads credentials without printing or persisting them, produces Module 0's checked communication artifact inside the bounded workspace, records the responsibility screen and frozen direction, observes their own falsifier fail, and knows the exact stop or escalation condition for anything still unavailable.

### 1.1 A reframing the need statement hides

The need as usually stated is "write good setup instructions." That framing has a measured failure rate. Mirhosseini and Parnin (ESEC/FSE 2020, *Docable*) executed 14,876 code blocks from 616 setup tutorials in fresh VMs: 13% ran naively, 26% with auto-patching, 52.3% with hand annotation — and **0 of 40 hand-annotated tutorials reached a final working setup**. The single largest error class was `E127 command-not-found` at 2,393 blocks, which the authors read as earlier setup steps having silently failed.

The correct framing is therefore: **a setup path is a program, and an unexecuted program is a broken program.** Prose quality is necessary and nowhere near sufficient. Any claim that five platform paths work, made without executing all five on clean machines, should be read as a prediction that at least one is broken right now. This Reference is built around that inversion, and §6 Class A exists only because of it.

### 1.2 What this module is not permitted to assume about its own author

Nathan and Petrosino (2003, n=48) found that domain experts significantly underestimate novice completion time, that intermediates predict better than experts, and that telling experts about the bias does not improve their predictions. Consequently: **no time budget in this document is authored.** Every duration below is either measured and cited, or marked `UNMEASURED` with the protocol that would settle it. An authored estimate presented as a budget is a defect under §6 D3.

---

## 2. Field survey

Fourteen systems, selected because each one settles a specific decision. Confidence is marked where it could not be verified from a primary source.

**2.1 Docable — Mirhosseini & Parnin, ESEC/FSE 2020** *(verified, primary)*. Executes tutorial code blocks in fresh VMs matched to the tutorial's OS, with assertions held in an external `steps.yml` selected by matching prose *above* each block — so the document cannot satisfy its own test. Asserts on **output**, not exit code, with the reason stated: some correct commands print to stderr. **Breaks:** Linux/SSH/VM only, so four of our five platforms are untestable by it; annotation cost is ~19 per tutorial. **Take:** the external stepfile, the output-not-exit-code rule, and the 0/40 number as our calibration baseline.

**2.2 Salerno, Treude & Thongtanunam, arXiv:2404.14637v3** *(verified, primary)*. The only think-aloud study of this exact audience: 24 sessions, 18 novices, 7 tools, plus 144 survey responses. Isolates **"Lack of Installation Progress Feedback" as its own failure category** (9/24 sessions) — beginners cannot distinguish hung from slow, or warning from error: *"I don't know if it's finished or not, how can I check?"* All four version-incompatibility cases were Apple Silicon. **Breaks:** students, one institution, no per-platform rates. **Take:** silence is the failure. Every step that is slow or quiet must state its expected duration and expected output volume before the learner runs it. Also: what learners *recall* blaming (unclear instructions, 88/144) is not what actually stopped them (process complexity, 14/24) — do not design from complaints.

**2.3 The Carpentries — `swc-installation-test-2.py`** *(verified)*. The strongest prior art for a learner-run, learner-unauthored check, and the only one designed for **bootstrap order**: stdlib-only, running on a machine where nothing is installed yet. Detects the OS with `platform` rather than asking the learner to self-identify, resolves failures through a `(system, package) → remediation URL` map, and uses OR-logic (`virtual-editor` passes on any of six editors) to test capability rather than brand. **Breaks:** unmaintained, not linked from the live install page, no fresh-shell check, no machine-readable output, hand-forked per cohort. **Take:** stdlib-only bootstrap design, auto-detected platform, and a remediation pointer on every failure.

**2.4 Degani & Wiener, *Human Factors* 35(2), 1993 (NASA CR-177549)** *(verified, primary)*. Guideline #1 is the most transferable rule in the survey: *checklist responses must portray the value or status of the item, not "checked" or "set"* — because *"'checked' and 'set' can be said too easily without any sound verification"* (ASRS 76798). Guideline #6: most critical items first, before interruption. Guideline #8: an explicit completion call. Names the real failure mode, **short-cutting**: collapsing several challenges into one response. **Breaks:** its core mechanism is two-operator challenge/response; a solo learner has no partner. **Take:** every verification response is a printed value compared against a shown exemplar — never a checkbox, never a learner-typed "PASS". The absence of a second operator is the argument for the executable check: the machine is the second crew member.

**2.5 The Rust Book ch. 1.1 + rustup** *(verified)*. Names an exact success string (*"Rust is installed now. Great!"*), gives expected output as a template with variable parts marked, and separates "installed" from "works" with a compile-and-run. **Take:** the exact-string success signal and the marked-variable output template.

**2.6 Flask's installation page** *(verified, negative exemplar)*. Lists commands with no expected output, no verification, and no failure branch. **Take:** what not to ship.

**2.7 Homebrew `brew doctor` / `diagnostic.rb`** *(verified)*. Broad environment diagnosis, but famously noisy: warnings that are almost always benign train users to ignore the tool. **Take:** a check that cries wolf is worse than no check. This is the argument for a three-state verdict (§4.4).

**2.8 Microsoft WinGet Configuration + Install WSL** *(verified)*. Declarative YAML with a first-class assert/apply split and idempotent resources. **Breaks decisively for us:** documented best-effort semantics — *"the configuration file will continue to run… even if some of the assertions or resource dependencies fail"*, leaving the learner to detect failures afterward. A partially configured machine plus a self-service detection burden is worse than a clean stop. **Take:** the assert/apply split; reject the partial-application semantics.

**2.9 Chef InSpec** *(verified)*. A cross-platform executable specification of a machine's desired state, with a human-readable control language and machine-readable output. **Take:** the idea that the environment specification is itself an artifact under version control, and that its output has a schema.

**2.10 `flutter doctor`, Docker `com.docker.diagnose check`** *(verified)*. Three-state output, per-check identifiers, and — in flutter's case — a next action per failure. **Take:** stable check IDs and next-action strings.

**2.11 `mise`, and Julia Evans on PATH** *(verified)*. Both target the activation gap: the tool is installed and still not found, because a shell did not load what it needed. **Take:** the fresh-shell check is not a nicety; it is the check for the single most common failure.

**2.12 Advent of Code and the CTF flag model** *(verified/partial)*. Per-participant input; the participant submits only the answer; the verdict is computed where the participant cannot reach. Because the flag is a **byproduct** of the work rather than a description of it, the entire challenge description and rubric can be published without weakening the check. **Breaks:** verifies the answer, not the method; and it needs somewhere to hold a secret — **which does not exist on the learner's own laptop.** AoC retired its global leaderboard for 2025 under capable models: verification survived, only speed ranking died. **Take:** never try to hide a secret on the learner's machine. Publish everything that is on the machine; hold the deciding artifact off it.

**2.13 okpy locked tests, GitHub Classroom autograding** *(verified from source)*. okpy's `locking.py` HMACs answers with `digestmod='md5'` keyed on **the assignment name** — a public string shipped in the same file, so a local model can enumerate short answers and match instantly. GitHub's own position on autograding tampering is *"we would not prevent student from editing but we can detect if a student change that."* **Take, stated falsifiably:** the secret must not be derivable from anything shipped to the learner. When the grader sits in the learner's tree, the honest design is not prevention but restore-over-detect plus a verdict computed elsewhere.

**2.14 METR, ImpossibleBench, "Building to the Test"** *(verified, primary)*. The decisive evidence for this module's architecture. METR: reward hacking occurred in **39/128 runs (30.4%) when the model could see the scoring function versus 8/1087 (0.7%) when it could not — a 43× difference**; on one task family, 21/21 = 100%; human baseliners hacked once. Prompting is not a fix: four honesty prompts left hacking at 70–95%, and o3 answered "no" to "does this plan adhere to the user's intention?" in 10/10 cases after producing a hacking strategy. ImpossibleBench: hiding tests drops cheating to near zero but degrades legitimate performance; **read-only access restores performance while preventing modification**. An explicit abort affordance cut hacking 54%→9% (GPT-5) and 49%→12% (o3); allowing multiple submissions *raised* it 33%→38%. Building to the Test: with a hidden oracle callable in-loop, every run scored 221–222/222 while up to 4 of 4 subsystems were dead. **Take, as three hard constraints:** (1) the deciding oracle's source must never sit in the learner's working directory; (2) acceptance must be two-part — behavioral *and* provenance; (3) give the learner a formative check that is **not** the deciding oracle, bound the retry budget, and provide an explicit "this looks impossible" escalation.

**2.15 RAID (ACL 2024), Liang et al. (*Patterns* 2023)** *(verified/partial)*. At a 5% false-positive operating point the best detector reaches 85.0% and most sit at 65–75%; a homoglyph attack costs Binoculars 41.9 points and Originality 75.7. Over 61% of TOEFL essays by non-native writers were flagged as AI-generated. **Take:** v1's refusal to accept a detector score as evidence is correct and well supported. It stands, now with citations.

### Measured numbers this Reference relies on

| Measure | Value | Source |
|---|---|---|
| Hand-annotated setup tutorials reaching a working setup | **0 of 40** | Docable §4.2 |
| Setup blocks executing naively | 13% (1,935/14,876) | Docable Table 1 |
| Largest error class | `E127 command-not-found`, 2,393 blocks | Docable Table 2 |
| Novices blocked by absent progress feedback | 9/24 sessions | Salerno Table 3 |
| Reward hacking, oracle visible vs hidden | **30.4% vs 0.7% (43×)** | METR |
| Prompting as a mitigation | leaves hacking at 70–95% | METR |
| Abort affordance as a mitigation | 54%→9%, 49%→12% | ImpossibleBench |
| Extra submissions as a control | raises cheating 33%→38% | ImpossibleBench |
| Simplified Technical English | task error rate 18%→14%, gains concentrated in non-native readers | Chervak, Drury & Ouellette, HFES 1996 |
| Words actually read on a page | ≤28%, "20% more likely" | Weinreich et al., ACM TWEB 2008 |
| Best AI-text detector at 5% FPR | 85.0%; most 65–75%; −41.9pp under homoglyph attack | RAID, ACL 2024 |
| Non-native essays falsely flagged | >61% | Liang et al. 2023 |

**Numbers that do not exist.** No published installation-failure rate, dropout rate, or setup-duration distribution for technical workshops. No instrumented time-to-first-value funnel for this kind of course. **Every setup-time and completion-rate figure in this document must therefore be produced by this module's own instrumentation, and is marked `UNMEASURED` until it is.**

---

## 3. Governing constraints and invariants

### Cannot be violated

1. **One command-line home per path.** Native Windows uses PowerShell; WSL uses Ubuntu Bash; macOS, Ubuntu and Arch use their native shell. A path never alternates.
2. **Linux work stays in the Linux filesystem.** WSL clones under `$HOME`, never `/mnt/c`. Windows GUI applications may open those files; command-line tools do not cross.
3. **No `sudo npm install -g`.** A user-owned npm prefix is configured before any global install.
4. **No blind remote execution.** The official source is named, the artifact is downloaded, and inspection precedes execution *in a separate step the learner completes before the installer runs*.
5. **No destructive default.** An existing course directory is inspected and preserved. No path removes a learner directory.
6. **Organizational policy is never weakened to make a step green.** A managed-machine block produces a support packet and a stop.
7. **A fresh-shell check is mandatory.** Persistent configuration must survive a new process; session-only secrets are re-entered by design.
8. **Function beats presence.** A version string cannot finish setup. Acceptance requires repository integrity, runtime execution, a local write, an authenticated AI write, and a clean rerun.
9. **The deciding acceptance control never resides on the learner's machine.** (§2.12, §2.13, §2.14.)
10. **No learner command block can terminate the learner's shell.** No `exit` or `return` at the top level of any block a learner is told to paste.
11. **Nothing the learner is told to do may dirty the course clone**, because clone integrity is itself a check.
12. **No secret, personal filesystem path, account identifier, or home directory appears in any committed file or generated report.**

### The tradeoff frontier

| Axis | Where the ideal sits | Why |
|---|---|---|
| Hidden oracle ↔ published oracle | **Publish the practice checker; hold only the deciding control off-machine** | METR's 43× applies to the *deciding* oracle. ImpossibleBench shows read-only access preserves legitimate performance. And the lab's own lesson requires the learner to read a checker. |
| Strict gate ↔ tolerant gate | **Three states: PASS / WARN / FAIL** | `brew doctor` (§2.7) proves a noisy binary gate gets ignored. Legitimate variance exists across five platforms; a binary check either false-fails healthy machines or passes broken ones. |
| Completeness ↔ parsimony | **Parsimony wins ties** | Every file, check, and section names the criterion it serves or is deleted. |
| Automation ↔ comprehension | **The learner runs the commands; the machine judges the result** | The objective is a capability, not a configured laptop. A one-click installer would satisfy the machine and fail the person. |
| Author's time ↔ learner's time | **Learner's time wins** | The author writes once; the failure repeats per learner per cohort. |

### Immovable context

- Five platforms, two of them Windows variants, one rolling-release.
- The learner owns the machine. There is nowhere on it to hide a secret.
- A capable AI assistant is present on the machine by design, and its use is legitimate.
- The course repository is public.
- Managed corporate laptops are expected, and some steps will be blocked by policy that the learner cannot change.

---

## 4. The ideal, characterized

### 4.1 Normal conditions

The learner opens the start page, identifies their platform in one table, and follows exactly one guide. Each step states its purpose, then the command, then the value they should see, then the condition that stops them, then where to go next. Long or silent steps state their expected duration and output volume in advance. At the end they close the terminal, open a new one, and repeat the proof. The machine, not the learner, decides whether it worked.

### 4.2 Edge conditions

- **Unsupported architecture** (Windows ARM64 where a required binary has no build): the path stops and names the alternative.
- **No desktop session:** Ubuntu's Obsidian step cannot complete. The path records the limitation explicitly and stops rather than pretending a browser screenshot is equivalent. *(v1 §5.D required a CLI-only alternative and simultaneously required a desktop; v2 resolves this in favour of the explicit stop — see `AMENDMENTS.md`.)*
- **Rolling-release drift** (Arch): observed versions are recorded, not assumed, and drift re-triggers the compatibility checks.
- **Pinned version withdrawn from a registry:** the check reports WARN with the observed version and the pin, not FAIL, and the learner continues to a recorded decision.
- **Existing clone or existing profile entries:** inspected, preserved, appended idempotently.

### 4.3 Adversarial conditions

The adversary is not a malicious learner. It is (a) an AI assistant on the learner's machine optimizing for a green result, and (b) an honest learner under time pressure taking the shortest path to "done."

- A model that reads the practice checker and writes a draft satisfying its literal strings while inverting the facts **must fail** — the practice checker is polarity-aware, and the deciding control is not on the machine.
- A learner who creates the missing file by hand after a tool claims to have written it **must fail** the tool-proof check on provenance, not only on content.
- A learner who edits the practice checker to pass **changes nothing**, because the practice checker was never the deciding control, and the module says so.
- A stub binary earlier on PATH **must fail**: checks record resolved absolute paths, not names.
- A secret entered by paste **must not** be silently captured from the following pasted line; credential entry is a single-command step run alone.
- An "impossible" state **has a named exit**: `HOLD` plus a support packet is a first-class, non-punitive outcome. (ImpossibleBench: an explicit abort affordance cut hacking 54%→9%.)
- **Retries are bounded**, because additional submissions measurably increase gaming (33%→38%).

### 4.4 Degraded conditions

Verdicts are three-valued and every non-PASS carries a next action:

| State | Meaning | Learner action |
|---|---|---|
| `PASS` | The check ran and the observed value matched. | Continue. |
| `WARN` | The check ran; the value is outside the expected set but the course can proceed. | Record it and continue. |
| `FAIL` | The check ran and the value blocks later work, or the check could not run. | Stop at this boundary, save the first error, use the support packet. |

A check that cannot run reports `FAIL` with the reason. Nothing silently degrades to `PASS`.

### 4.5 Ten times the scale or duration

- **200 learners:** case rotation and custody controls are unchanged; scale never justifies a shared answer key. Per-learner protected-control results are recorded pseudonymously.
- **Eighteen months:** pins drift. Every pin lives in one file, is machine-read by both verifiers, and has a recorded check date and update rule.
- **A second course, a second repository:** the coupling to this repository's remote and path layout is a named constraint with a migration note, not an assumption buried in five guides.

### 4.6 Budgets

All figures marked `UNMEASURED` are planning placeholders that the first pilot replaces. Under §1.2 they are not authored standards.

| Measure | Target | Status |
|---|---|---:|
| Setup, existing supported machine | 60–120 min | `UNMEASURED` |
| Setup, new WSL install including reboot | 90–180 min | `UNMEASURED` |
| Fresh-shell verification | < 5 min excluding credential entry and model latency | `UNMEASURED` |
| Managed-machine escalation | stop within 15 min of a proved policy boundary | `UNMEASURED` |
| **Facilitated session** | **180 min** | fixed by `COURSE_MAP.md` |
| **Learner working time inside it** | **120 min** | fixed by `COURSE_MAP.md` |
| First checked artifact | within 60 min of lab start | gate condition |
| Free disk | 15 GB; 25 GB for WSL | measured by the verifier |
| RAM | 8 GB floor, 16 GB recommended | not enforced |
| Provider spend | three short proof calls plus lab calls; recorded, never estimated | `UNMEASURED` |
| Correction attempts on a failed check | 2, then `HOLD` | bounded by design (§4.3) |

The 180/120 split is the single source of truth. The lab timebox and the facilitator schedule are both derived from it and must sum to it (§6 D3).

### 4.7 The experience

**First ten seconds.** The learner sees what the setup will make possible, a five-row table with exactly one row for their machine, how long to reserve, what "ready" looks like, and one warning: do not paste a key into a command, a file, or a screenshot.

**What they stop having to think about.** Whether they picked the right path. Whether a step "counted." Whether silence means broken. Whether they are allowed to stop. Whether their own judgment about the AI's output matters — the module makes it the only thing that decides.

---

## 5. Off-axis frontier

Five approaches differing in kind. The conventional design — five single-path tutorials, a stdlib-only fresh-shell checker, and a deciding control held off-machine — wins, and the value here is that it was chosen.

**F1 · Publish the whole witness; buy integrity from pool size.** *(FCC/NCVEC, 47 CFR §97.523: the published question pool must hold ≥10× the questions one exam needs.)* Integrity from ratio, not secrecy. **Buys:** retires the unwinnable problem of hiding a checker on hardware the learner owns, and makes the checker a teaching object the learner is told to read. **Costs:** the ratio must be real, and the second half of the mechanism — a live independent examiner — does not transfer to a self-paced laptop. **Adopted in part:** the practice checker is published and the learner is told to read it; the deciding control is held by the evaluator.

**F2 · Score, don't gate — assigned value plus tolerance band.** *(ISO/IEC 17043:2023, ISO 13528:2015: z = (result − assigned)/σ, |z| ≤ 2 satisfactory, 2–3 questionable, > 3 unacceptable.)* **Buys:** a principled three-state lattice; fixes the false-failure brittleness that made `brew doctor` ignorable; and with N learners reporting, produces the per-platform distribution the field has never published. **Costs:** ceremony on facts that are genuinely binary. **Adopted in part:** the three-state verdict and its interpretation; not the statistics.

**F3 · Ship an executable manifest, not a document.** *(WinGet Configuration; Brewfile + `brew bundle check`.)* **Buys:** attacks the largest measured failure — the E127 cascade exists because humans execute sequences and silently miss steps. **Costs:** WinGet's best-effort partial-application semantics are an anti-pattern for this audience; a non-developer cannot audit a DSC manifest; and it does not exist in equivalent form on all five platforms. **Deferred:** viable later as a signed fast path with a manual fallback and an independent post-check.

**F4 · Dissolve it — the runtime ships inside the page.** *(Pyodide, JupyterLite.)* **Buys:** identical environment on all five platforms; no install, no account, no Docker licence. **Costs:** it dissolves the capability along with the problem — the learner never opens a shell and cannot debug their own laptop afterward, which is the objective. **Adopted as a fallback only:** for a learner hard-blocked by IT, explicitly marked as not satisfying the local-setup objective, with its usage rate instrumented — that rate is the per-platform failure number the field does not publish.

**F5 · Grade the repair, not the install.** *(Chaos engineering; DeMillo/Lipton/Sayward mutation testing, 1978.)* Seed a known fault — a stub `python` earlier on PATH, an unsourced rc file, WSL resolving the Windows binary — and grade the recovery. **Buys:** targets the capability the whole survey says is missing, and is immune to building-to-the-test. **Costs:** wrong for a first lab — the learner has no model of "correct" yet, and it inverts the emotional register exactly when learners quit. **Adopted in part, and this is the highest-value graft in the section:** the mutant list becomes the oracle's own pre-ship adequacy test. Every mutation must be killed. The exercise itself belongs to a later module.

**Why the conventional design still wins.** F1, F2 and F3 are grafts onto it; F4 is a fallback from it; F5 is a sequel to it. The two that look like genuine alternatives fail on the objective rather than on execution — F4 removes the shell, F5 assumes the competence the module exists to create.

---

## 6. The acceptance oracle

The governing principle, and the one v1's oracle violated: **a check that has never failed proves nothing.** Every criterion names both its check and at least one input the check must reject. A criterion with no negative fixture is not a criterion.

Checks live in `tests/` and run with `python3 tests/test_module_00.py`. Mutation fixtures live in `tests/mutations/`; each is applied to a temporary copy of the module and must produce the named failure.

### Class A — the module is reachable, runnable, and cannot strand the learner

| ID | Criterion | Check | Must reject |
|---|---|---|---|
| A1 | Every clone-relative path a learner is told to execute exists in the repository. | Extract paths from all fenced blocks; assert each exists. | a guide citing an uncommitted path |
| A2 | The module is tracked by git; on-disk file count equals `git ls-files` count. | git plumbing | the untracked state v1 shipped in |
| A3 | No learner block can terminate the learner's shell. | no `exit`/`return` token at top level of any fence in learner files | a fence containing `exit 1` |
| A4 | Every block using a relative path first establishes its directory in the same block. | per-fence `cd`-before-relative-path check | Ubuntu step 8 as v1 shipped it |
| A5 | Following the guide cannot dirty the clone. | `.obsidian/` ignored; simulated vault-open leaves `git status --porcelain` empty | a `.gitignore` without `.obsidian/` |
| A6 | Every fence parses in the shell it declares. | `bash -n`, `zsh -n`, PowerShell parser, `python -m py_compile` | a fence with unbalanced quotes |
| A7 | No block can persist an empty PATH element. | static scan for `::`, leading/trailing `:` in any `PATH=` assignment; runtime check in both verifiers | macOS step 4 as v1 shipped it |
| A8 | Credential entry is a single-command step, run alone. | the fence containing the hidden-input read contains exactly that command | a multi-line fence containing `read -r -s` |
| A9 | Every step that is slow or silent states its expected duration and output volume. | each install/download fence is preceded by a duration annotation | an unannotated `brew install` |
| A10 | Inspection of a downloaded installer completes before it executes. | download, inspect and execute are in separate fences, in that order, with the "what to look for" text before the execute fence | the Windows goose block as v1 shipped it |

### Class B — the acceptance machinery discriminates

| ID | Criterion | Check | Must reject |
|---|---|---|---|
| B1 | The practice checker rejects a draft that inverts a reader-affecting fact. | fixtures: inverted cost, inverted eligibility, inverted entrance | v1's substring checker |
| B2 | The practice checker rejects a draft asserting any of the six unconfirmed services. | one fixture per service | v1's checker |
| B3 | Every numeric claim is bound to its subject, not matched loosely. | fixture: correct capacity 45 while mentioning the former 60 | `\b60\b` |
| B4 | A correct changed-input revision **fails** the original checker, exactly as the lab tells the learner it will. | fixture run against the original checker → non-zero, naming capacity | v1: it passed, making the lab's statement false |
| B5 | Faithful paraphrase passes. | fixtures: "no charge", "Sixty people", "ID is not needed" | brittle literal matching |
| B6 | Every check in the practice checker has at least one killing fixture, asserted by the module oracle. | fixture-coverage assertion | a checker with unfixtured checks |
| B7 | The deciding acceptance control is not present, derivable, or reconstructable from anything in the repository. | scan for graded cases, expected answers, or keyed digests | a graded checker committed to the repo; an HMAC keyed on a public string (§2.13) |
| B8 | The tool-proof check verifies provenance, not only content. | a hand-created file with correct content fails | v1: three `printf` calls satisfied it |
| B9 | The n8n check verifies n8n, not any listener on the port. | `python3 -m http.server 5678` must fail the check | v1: it passed |
| B10 | Retry budget is bounded and stated. | two correction attempts then `HOLD`, in lab and rubric | unbounded retries (raises gaming 33%→38%) |

### Class C — the oracle cannot be defeated by editing a file it does not read

| ID | Criterion | Check | Must reject |
|---|---|---|---|
| C1 | The scan set is derived by glob and its count asserted against the enumerated set. | glob all `.md`/`.py`/`.sh`/`.ps1` under the module | v1: `REQUEST.md` and `CHANGED_INPUT.md` were scanned by nothing |
| C2 | The safety scan reads every fence regardless of info string. | scan all fences | a ```text fence containing `sudo npm install -g` |
| C3 | Pins are parsed from `VERSIONS.md` and asserted per file, never by concatenation. | per-file assertion | one guide with a wrong pin masked by four correct ones |
| C4 | Each absolute failure in §10 has a dedicated check and a killing fixture. | one fixture per absolute failure | v1: three simultaneous absolute failures passed |
| C5 | Structural criteria are per-unit, not per-file. | count terminal labels against fences requiring one; count stop conditions against install sections | v1: one label anywhere in a file satisfied "every command block" |
| C6 | The oracle fails when the module is mutated. | every fixture in `tests/mutations/` produces its expected failure ID | any mutation passing |
| C7 | No learner-facing file contains internal curriculum language, a product token, or a personal path. | forbidden-token scan over globbed learner files, including absolute-path patterns | `GAUNTLET_PROMPT.md` as v1 shipped it |

### Class D — claims match artifacts

| ID | Criterion | Check | Must reject |
|---|---|---|---|
| D1 | Every evidence row names a command that reproduces it. | each row in the verdict has a command and stored output; re-running reproduces | "171 PASS" with no negative meaning |
| D2 | Every human score cites reviewer role, revision, rubric, and — for any deduction — the quoted sentence. | `reviews/` contains one file per reviewer | v1: four 40/40 scores and an empty `reviews/` |
| D3 | Lab timebox, facilitator schedule, and this document's budget agree. | arithmetic assertion: lab sum == runbook learner span == 120 min | v1: 180 / 150 / 120 |
| D4 | Every deviation from this Reference is recorded. | `AMENDMENTS.md` enumerates each; oracle asserts the count | v1: the headless-Ubuntu refusal was unrecorded |
| D5 | Platform execution status is stated per platform and never inferred from static checks. | verdict table; no "verified" without a named run | claiming five-platform delivery from a macOS session |

### Class E — the learner records satisfy the skeleton gate

Traced to `reformation/modules/core/00-direct-bounded-work.md` and `LEARNING_OBJECTIVES.md` PO-00.

| ID | Criterion | Check | Must reject |
|---|---|---|---|
| E1 | A capability-limit statement is a required record with a rubric gate: model output vs product surface vs harness control vs human decision, plus one observed capability and one observed limitation. | lab template + rubric row + oracle assertion | v1: absent entirely |
| E2 | The learner **runs** their stated falsifier and records its visible failure. | lab step + rubric row + required field | v1: the falsifier was only stated |
| E3 | The protected acceptance control is confirmed before work begins, and its result is a required record. | lab step 1 + rubric row | v1: replaced by an unseen second case |
| E4 | Setup is an entry condition, not a PO-00 hard gate. | rubric contains no setup gate | v1: a broken n8n held PO-00 |
| E5 | Every filesystem action the lab requires has an exact command and an expected observation. | each imperative has a fence | v1: "create a folder", "copy the files" — prose only |
| E6 | The module is scored on its supplied case with a protected acceptance control, per the course skeleton — not on a separate unseen case. | rubric, runbook and custody contract agree | v1: a 20-minute unseen graded case with no skeleton basis |

### Class F — the prose serves the reader

Scored by a three-person panel: one technical beginner, one experienced cross-platform operator, one professional editor. Each dimension 0–4; **acceptance requires 32/32 from every reviewer**, with any deduction citing a specific sentence. A numeric AI-detector result is **not** accepted as evidence (§2.15: best detector 85.0% at 5% FPR, −41.9pp under trivial attack, >61% false-flag rate on non-native writers).

1. Sounds like someone who has done the task.
2. States purpose before action.
3. Ordinary complete sentences.
4. Exact, concrete detail without display.
5. Treats failure as diagnostic evidence.
6. No generic encouragement, hype, throat-clearing, or repeated summary.
7. Preserves the learner's agency.
8. Reads aloud without sounding generated.

| ID | Criterion | Check |
|---|---|---|
| F1 | Every unfamiliar term used in an instruction is defined at first use — including PATH, which heads a section in all five guides. | glossary assertion + editor review |
| F2 | No learner-facing file explains why the course is built the way it is. | reviewer pass against the discriminator in `CLAUDE.md` |
| F3 | Accessibility guidance names real assistive technology and gives real operations, or states honestly that a path is unverified. | operator review |
| F4 | Every "Stop here if" names an observable condition, not a judgment. | editor review |

### Failure conditions — any one means this is not the ideal, whatever else scores

- **X1** A learner following one guide verbatim on a supported platform reaches a state the guide does not name.
- **X2** The oracle passes a module tree containing any absolute failure from §10.
- **X3** The practice checker passes a draft that inverts a reader-affecting fact.
- **X4** Any check in the suite has no negative fixture.
- **X5** Any learner-facing file contains making-of content.
- **X6** A secret, personal path, account identifier, or home directory appears in any committed file or generated report.
- **X7** An evidence row claims a result that no stored command reproduces.
- **X8** The deciding acceptance control, or anything from which it can be reconstructed, is present on the learner's machine.

---

## 7. Anti-goals

Excellence here explicitly does **not** include:

- **A one-click installer.** It would satisfy the machine and fail the person. The objective is a capability.
- **Teaching the toolchain.** n8n and Obsidian are installed now so machine work does not interrupt a later session. Their presence is not a Module 0 objective, and no Module 0 gate may depend on them.
- **A troubleshooting encyclopedia.** The tree starts at the first failed boundary and stops. It is not a catalogue of every error on the internet.
- **A sixth platform, a container path, or a cloud IDE as a first-class route.** WASM exists as a named fallback (§5 F4) and nothing more.
- **Detecting AI-written prose.** Not scientifically supportable (§2.15). The panel cites sentences instead.
- **Preventing a determined learner from cheating on their own machine.** Not achievable (§2.13) and not the goal. The design makes cheating pointless — the deciding control is elsewhere — rather than impossible.
- **Scoring the setup.** Setup is an entry condition.
- **Generality.** No abstraction with one implementation. No extension point nobody asked for.
- **Reference-implementation prose in the learner path.** Design rationale belongs in this file.

---

## 8. Obsolescence

This Reference is wrong within eighteen months if any of the following happens; the earliest visible signal is given.

| What would invalidate it | Earliest signal |
|---|---|
| A pinned tool changes its CLI surface or version scheme | the verifier's exact-match check reports WARN across a cohort |
| Codex, OpenCode or goose consolidates, is renamed, or changes auth | `codex login status` or a provider flag fails on a clean install |
| Node 24 leaves LTS, or n8n's engine floor moves past it | `npm view n8n engines` disagrees with `VERSIONS.md` |
| Windows ARM64 gains full binary coverage | the goose Windows installer publishes an ARM64 asset |
| Homebrew retires `python@3.12` or `node@24` | `brew --prefix` returns empty in the pilot |
| Reformation moves to its own repository | the remote coupling constraint is triggered; five guides and two verifiers change together |
| Agentic assistants gain reliable machine-level sandboxing the learner cannot escape | a deciding control could then live on-machine, and §3 invariant 9 could relax |
| A defensible AI-text detector appears | RAID-class benchmarks show >95% at 1% FPR with no accent bias; §6 Class F could then change |

The most likely single cause of drift is the version pins. They live in one file, are machine-read, and carry a check date for exactly this reason.
