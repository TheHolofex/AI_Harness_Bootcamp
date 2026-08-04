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

**Bounds:** one baseline. Three search agents. At least two rounds and at most three. At most twelve findings carried into verification. Two verifiers, splitting those findings between them. One merge. One provenance check. One package. A run that wants more than this has not been divided properly.

### Stage 1 — One agent, saved

Run the need through a single agent. Save the result untouched and do not read it yet — you write the measures next, and knowing what this run missed will bend them toward flattering the fan-out.

**You direct:** the brief that agent gets, and the run identity saved beside it — engine, model, corpus, date.

**Working when:** the result is saved before anything else runs, you can still open it at the end of the afternoon, and when you do you can name what the fanned-out run has that this one does not. If you cannot, the fan-out did not pay for itself and saying so is the correct result.

*Skill: knowing when to fan out*

### Stage 2 — Put the measures into the run

Coverage and support defined for this need, written where the run applies them rather than in a document. A finding either meets them or it does not.

Coverage is what the decision obliges an answer to settle — each obligation addressed or openly unaddressed. Support is whether a kept finding rests on a source that actually carries it. You are not measuring recall: recall needs a known set of everything relevant in the corpus, nobody has one, and a measure you cannot compute is a measure you will end up faking.

**You direct:** what the decision obliges an answer to settle, and what makes a finding worth keeping.

**Working when:** the measures would read differently if the need were different, the run can sort findings by them without a person, and neither one needs a list of right answers that does not exist.

*Skill: measuring the right thing*

### Stage 3 — Fan out on different search paths

Several agents, each searching a genuinely different way: by source type, by entity, by time window, by what someone arguing the opposite would have looked for. Same question, different routes in.

They reach the corpus through one read-only local server, not through the filesystem. What an agent may not look at is then a property of the surface it was handed, rather than a sentence in its instructions that it is free to ignore.

**You direct:** what makes each route different, what each agent's surface exposes and therefore what it cannot reach, and what each must record about its own search — files opened, queries run, findings, and the citation under each one.

**Working when:** the routes differ in what they read, not in what they return. Two agents landing on the same important fact is corroboration, not waste. Compare the files opened, entities searched, windows covered and exclusions set; if those match, the routes were never different, whatever came back. An agent told to search outside its route should be unable to, not merely unwilling.

*Skill: work division*

### Stage 4 — Let the run decide when it is done

Rounds continue until one comes back with nothing new, or until the ceiling stops them. The run applies both rules and says which one fired.

**You direct:** what counts as new, the least number of rounds that must run before nothing-new can mean anything, and the ceiling.

**Working when:** the search ends on its own rule and names which. A run stopped by the ceiling finishes as work left unresolved, not as complete — and that is a legitimate way to finish. One empty round straight after the first pass is not saturation; it is a slow start.

*Skills: knowing when to fan out, work division*

### Stage 5 — Verifiers that only refute

Findings are split across a fixed few agents whose instruction is to knock them down against the sources. They add nothing. A finding survives the attempt or it does not.

**You direct:** what a verifier may use, how the findings are divided between them, and what defeats a finding.

**Working when:** findings are dropped by the verifiers rather than by a person reading carefully, and you can see which ones died and why. One current authoritative source that contradicts a finding kills it however many challenges it survived — this is not a vote. Surviving a challenge is not the same as being true, and nothing downstream may say it is.

*Skill: measuring the right thing*

### Stage 6 — Merge under a stated rule

One instruction to the orchestrator covering what happens to disagreement, what carries more weight, and how confidence moves through. Three workers saying "probably" cannot come out the other side as "certainly." Confidence may rise when two sources that do not depend on each other both carry the claim. It may never rise because more agents repeated it.

Run that instruction twice: once on the model doing the rest of the work, and once on a model from a different family, called as a single headless job and read from its output rather than trusted to write anything of yours. Then pick the one you ship. Putting the more capable model where the judgment concentrates is the decision; running both is how you find out where that is.

**You direct:** the conflict rule, the weight rule, the confidence rule, and which merge you ship — with the reason it is that one, and not simply the model you use for everything.

**Working when:** the merged answer reads as one decision rather than several reports side by side, no claim leaves the merge more certain than its evidence, and wherever confidence did rise you can name the independent source that raised it. The reason you give for the merge you shipped is something you saw in the two of them, not a preference you brought with you.

*Skill: directing the merge*

### Stage 7 — A provenance check that fails loudly

A step that walks every claim in the finished product back to a source and fails the run when one cannot be walked. It runs against the same surface the search used, so a claim citing something that surface will not serve fails on that alone. It checks that the source exists, that it is the one cited, and that the quoted words are in it. It cannot check that the source means what the claim says. That judgment stays yours, and the run must never present the check as though it made it.

**You direct:** what counts as a live source — one the surface will still serve today, not one that was there when the search ran — and which claims you read yourself.

**Working when:** it fails on a claim you plant with no source behind it, on one whose quote you alter, and on one citing a source that has since been superseded — and it passes without a person checking anything by hand, while the finished product still separates what the check proved from what you judged.

*Skill: preserving provenance*

### Stage 8 — Save the run so it executes again

The orchestration packaged alongside the morning's plugin work, so the next version of this question runs it rather than being rebuilt.

The package also declares the domain it was tuned for — which family of work the next question will come from. A method that travels has to say what it was built against, or the person who reuses it on something else will not find out until the answer is already wrong.

**You direct:** what is fixed in the package, what is supplied fresh each time, and the domain the package declares.

**Working when:** the package names every input the run needs — the declared domain among them — carries none of this question's answers, and someone reading its contents can say exactly what they would have to supply to ask a different question of the same shape. Running it against that different question is the proof, and it is not this afternoon's work — do not claim it as done.

*Skill: portable packaging, carried from the morning*
