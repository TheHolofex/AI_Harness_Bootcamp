# Tuesday exercises

---

## Morning — Inbound

People arrive. Someone works out who they are, what they can do, what they need, and what has to reach them. Today that sits in one person's head and breaks when they leave. By the end of the morning it runs as a set of components that regenerate from source.

**Material:** an inbound roster in three or four formats, source records covering billets and capabilities, the distribution lists as they stand today, and a pile of messages carrying directives.

### Stage 1 — Normalize on the way in

A hook that fires on intake and turns whatever arrives — a spreadsheet, pasted text, an export from another system — into one shape before the model sees any of it. Missing fields stay missing and say so. Nothing gets invented to fill a column.

**You direct:** what the one shape is, and what the hook does with a file it cannot parse.

**Working when:** you drop in a format it has never seen and it either normalizes it or refuses it loudly. It never passes something through half-converted.

*Skill: enforcement design*

### Stage 2 — Map people to capabilities

A skill that reads the normalized roster and produces the capability mapping. Where the source does not say, the mapping says it does not know.

**You direct:** the description that makes it load on its own, and what counts as enough evidence to assert a capability rather than infer one.

**Working when:** it fires on a roster you did not write it for, and stays quiet on a document that is not a roster.

*Skill: building what earns its place*

### Stage 3 — Generate the distros

A skill that produces the distribution lists from the mapping. Generated every time, never hand-edited. Updating stops being an editing job and becomes a rerun.

**You direct:** the rule for who lands on which list, and what happens to a person the mapping could not place.

**Working when:** you change one person's capability in the source, rerun, and only the lists that should change do.

*Skill: building what earns its place*

### Stage 4 — Refuse a change that cannot name its source

A hook that blocks any distro output containing a line that cannot be traced back to the record that put it there.

**You direct:** what counts as a source, and whether the hook blocks or marks and continues.

**Working when:** you hand-edit one line into a list and try to ship it, and it gets stopped.

*Skill: enforcement design*

### Stage 5 — Narrow it until it would survive

Run the whole set against material it should ignore: a message thread, an unrelated spreadsheet, a roster from a different process. Anything that fires when it should not gets narrowed until it stops.

**You direct:** the line between what it acts on and what it leaves alone.

**Working when:** nothing fires on the out-of-scope material, and everything still fires on the material that is in scope.

*Skill: blocking only what should be blocked*

### Stage 6 — Find out why something did not fire

Break one thing. Change a source format, alter a trigger word, move a file. Something stops working.

**You direct:** nothing yet. Read the record first and find out whether it loaded, ran, or was never reached.

**Working when:** you can name which of the three it was before you change anything, and the fix is one line rather than a rewrite.

*Skills: seeing what is loaded, failure diagnosis*

### Stage 7 — Package it

One plugin carrying the hooks, the skills, and the configuration.

**You direct:** what belongs inside the package and what is genuinely outside it.

**Working when:** the contents account for every part of the working set, nothing points at a path only you have, and no secret is inside it.

*Skill: portable packaging*

---

## Afternoon — The information need

A question that will be asked again. Answering it once is not the job; answering it well enough to defend, and again next month without rebuilding, is.

**Material:** one information need with a real decision behind it, and a corpus spread across several source types.

### Stage 1 — One agent, saved

Run the need through a single agent. Save the result untouched. Everything after this has to beat it.

**You direct:** the brief that agent gets.

**Working when:** the result is saved before anything else runs, and you can still open it at the end of the afternoon.

*Skill: knowing when to fan out*

### Stage 2 — Put the measures into the run

Recall and precision defined for this need, written where the run applies them rather than in a document. A finding either meets them or it does not.

**You direct:** what counts as covered, and what counts as relevant enough to keep.

**Working when:** the measures would read differently if the need were different, and the run can sort findings by them without a person.

*Skill: measuring the right thing*

### Stage 3 — Fan out on different search paths

Several agents, each searching a genuinely different way: by source type, by entity, by time window, by what someone arguing the opposite would have looked for. Same question, different routes in.

**You direct:** what makes each route different, and what each agent is not allowed to look at.

**Working when:** the returns do not overlap heavily. Two agents bringing back the same set means the routes were not different.

*Skill: work division*

### Stage 4 — Let the run decide when it is done

Rounds continue until one comes back with nothing new. The run applies the rule.

**You direct:** what counts as new.

**Working when:** the search ends because a round found nothing, not because the clock ran out.

*Skills: knowing when to fan out, work division*

### Stage 5 — Verifiers that only refute

For each finding, agents whose instruction is to knock it down against the sources. They add nothing. A finding survives the attempt or it does not.

**You direct:** what a verifier may use, and how many have to fail before a finding is dropped.

**Working when:** findings are dropped by the verifiers rather than by a person reading carefully, and you can see which ones died and why.

*Skill: measuring the right thing*

### Stage 6 — Merge under a stated rule

One instruction to the orchestrator covering what happens to disagreement, what carries more weight, and how confidence moves through. Three workers saying "probably" cannot come out the other side as "certainly."

**You direct:** the conflict rule, the weight rule, the confidence rule, and which model runs the merge — with the reason it is that one.

**Working when:** the merged answer reads as one decision rather than several reports side by side, and no claim leaves the merge more certain than it entered.

*Skill: directing the merge*

### Stage 7 — A provenance check that fails loudly

A step that walks every claim in the finished product back to a live source, and fails the run when one cannot be walked.

**You direct:** what counts as a live source.

**Working when:** it fails on a claim you plant with no source behind it, and passes without a person checking anything by hand.

*Skill: preserving provenance*

### Stage 8 — Save the run so it executes again

The orchestration packaged alongside the morning's plugin work, so the next version of this question runs it rather than rebuilding it.

**You direct:** what is fixed in the package and what is supplied fresh each time.

**Working when:** a new question of the same shape runs end to end without the run being reassembled.

*Skill: portable packaging, carried from the morning*
