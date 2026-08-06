# The watch officer · AI controls the workboard

---

## Opening lab — Ten Agentic Patterns in Pi

| Objective | Skill | Builds on | What is new | What mastery looks like |
|---|---|---|---|---|
| **1. Turn named patterns into executable control flow.** | Pattern implementation | Wednesday's control-flow presentation | Ten supplied Pi programs make the control structure visible in code and in the runtime trace: prompt chain, routing, parallel fan-out/fan-in, orchestrator-workers, handoff, evaluator-optimizer, tool loop, planner-executor, reflection, and supervisor with subagents as tools. | All ten implementations end in their named PASS lines, and the final verifier reports `PI LAB VERIFY PASS patterns=10`. |
| **2. Distinguish patterns by the path work takes.** | Trace reading | Tuesday's work division and Wednesday's durable state | The same Pi runtime is held constant while delegation, state, tools, evaluation, and synthesis change from file to file. | You can identify the pattern from its printed trace and point to the source file that implements that flow. |

> **After the lab:** You have run ten common agentic patterns as working Pi programs and can recognize each one by its implementation and trace.

---

## Morning — The watch officer

| Objective | Skill | Builds on | What is new | What mastery looks like |
|---|---|---|---|---|
| **1. Hand over an outcome, not a list of steps.** | Mission shaping | Monday's rerunnable product | Monday made a useful product repeatable. This gives an agent the finish state and lets it choose how to reach it. | Your mission is short because the desired state is precise. You are not feeding the agent its next action one message at a time. |
| **2. Let feedback choose the next action.** | Closed-loop delegation | Tuesday's unattended workers | Tuesday dispatched a bounded batch. Full Goose can inspect, build, run the checker, and use its findings while the mission is still underway. | You can point to checker feedback that changed the work, and the agent stops only when the final result says `P6 VERIFY PASS`. |
| **3. Revise one living product as the world changes.** | Stateful revision | Monday's delta test and Wednesday's durable state | Earlier work rebuilt or retrieved a product. This revises the same `command_center.html` and `mission_state.json` when late evidence arrives. | Current facts stay coherent, sound work remains, and the page visibly separates `NEW`, `CHANGED`, `CANCELLED`, and `UNCHANGED`. |
| **4. Intervene once where judgment is worth more than supervision.** | Consequential steering | Monday's live correction and judgment ownership | Goose makes a defensible provisional judgment in Wave 1. You select one complete operator intent in Wave 2, and the agent replans around it. | Your exact intent appears in the state and command center. You steer the outcome without becoming the agent's project manager. |
| **5. Read the work compressed by the mission.** | Recognizing agentic leverage | Tuesday's work division | Tuesday divided a question among workers. This identifies the planning, correlation, checking, and revision that two autonomous launches coordinated through one persisted mission state. | You can name the hours and handoffs the mission compressed, the part that still needed you, and one real workload where that trade would be useful. |

> **After the morning:** You can give an agent a changing operational objective, let it choose and revise the work needed to reach a checked finish, and steer the result with one decision instead of directing every step.

---

## Afternoon — AI controls the workboard

| Objective | Skill | Builds on | What is new | What mastery looks like |
|---|---|---|---|---|
| **1. Turn spreadsheet rows into structured production work.** | Designing an AI spreadsheet station | Monday's repeatable judgment product | Monday made one judgment product rerunnable. This lets n8n read each workbook row and gives AI eight named columns to fill so later nodes can use the result without reading prose. | All 60 first-wave rows return to `workboard.xlsx` with workstream, priority, summary, next action, and policy fields populated. |
| **2. Route rows through visible branches and write them back.** | Visual fan-out, fan-in, and XLSX writeback | Tuesday's work division | Tuesday split one question across several agents. This uses one spreadsheet field to send rows to specialist branches, apply policy, recombine them, and overwrite the workbook. | The n8n canvas visibly carries the rows through four branches and back into one 60-row `AI Workboard` sheet. You can trace one identifier from its source row to the written result. |
| **3. Change one rule once and watch the spreadsheet move.** | Rule leverage | Monday's delta reading | Monday showed what changed between reruns. This changes policy at one branch and measures the effect in the workbook without repairing records one at a time. | Side-by-side workbook copies name the Operations rows and four columns that changed. The row-by-row edit count is zero. |
| **4. Put new rows through the same saved machine.** | Second-wave operation | Monday's rerunnable product and the morning's changed-world run | Earlier work reran a product or let an agent revise its plan. This adds 20 source rows to the workboard and uses the same visual graph, prompt, schema, routes, and writeback. | Rows 61–80 begin with blank AI columns and return populated. The final workbook and receipt account for 80 total rows. |
| **5. Choose a fixed, adaptive, or hybrid machine for real work.** | Machine choice | The morning's adaptive loop | The morning showed work whose next step changes with feedback. This separates that work from repeatable production and from systems that place adaptive work inside a designed outer line. | You classify one earlier course workload plus two desk workloads—or two distinct parts of one desk workload—as fixed, adaptive, and hybrid, then defend each choice with path variability and evidence of leverage. |

> **After the afternoon:** You can make n8n read a spreadsheet, use AI to structure every row, route the rows through visible policy branches, and write the result back; then change one rule once, run a second wave through the same graph, and choose fixed, adaptive, or hybrid for real work.
