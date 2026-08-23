# Read a mission thread without getting lost in it

Plan for 15 minutes. This page gives you the only logistics model you need for the Cold Lantern case.

## What a mission thread is

A **mission thread** is the ordered path from a request to a result. It shows what must happen, in what order, and what each step must hand to the next.

Cold Lantern uses eight steps:

1. **Requirement defined** — the destination, usable quantity, route, and deadline are clear.
2. **Cargo received** — the warehouse records the exact totes and lots in its custody.
3. **Cargo released** — the quality office identifies which lots may be used.
4. **Vehicle made ready** — the released load and required rack fit the vehicle.
5. **Movement authorized** — the permit applies to the exact vehicle and route.
6. **Route window met** — the vehicle can reach the gate before it closes.
7. **Cargo delivered** — the route can reach the clinic by the deadline, and later evidence records actual delivery.
8. **Usable effect confirmed** — the clinic records receipt of the required released quantity.

The decision is whether the supplied evidence supports a `GO` brief at step 6. Expected arrival does not prove delivery or clinic use.

## Why a thread becomes difficult

Each step looks simple until you ask what its words mean.

“Cargo received” opens into smaller questions:

- Were the exact totes scanned?
- Do their lot IDs match this mission?
- How many kits are in each tote?
- Does the warehouse record custody, or does it also have authority to release the kits?
- Was the record current at the decision time?
- What does the next step require?

The same pattern repeats inside every step. Check these seven parts when they matter:

| Part | Plain question |
|---|---|
| Identity | Is this the exact mission, route, vehicle, permit, lot, clinic, and source revision? |
| Authority | Is this source allowed to establish this kind of fact? |
| Time | Was it current at 14:05 MDT, and is its time zone understood? |
| Quantity or condition | Are the count, units, required equipment, and state correct? |
| Dependency | What had to be true before this step could begin? |
| Handoff | Does this step's output meet the next step's entry condition? |
| Uncertainty | What is unknown, assumed, contradicted, or not yet observed? |

Do not keep splitting a claim forever. **Stop decomposing** when you reach one of these:

- a fact you can read directly in an applicable source;
- a calculation you can reproduce from supported facts and units;
- an assumption you have named as an assumption;
- an unresolved item that requires `HOLD`; or
- a decision owned by a named person.

## Five kinds of statement

Use one label for every material statement in the AI brief:

- `SOURCE FACT` — an applicable source directly states it.
- `CALCULATION` — supported numbers and units produce it.
- `INFERENCE` — you interpret facts and state why that reading follows.
- `DECISION` — a named person chooses what happens next.
- `UNSUPPORTED` — no applicable source or sound calculation establishes it.

A sentence can contain more than one kind. Split it until each row has one kind.

## Source authority belongs to the claim

A source is not trustworthy for everything.

- The warehouse records what it scanned.
- The quality office decides which lots are released.
- Fleet Engineering defines vehicle payload and required equipment.
- The Road Authority sets the gate window.
- The Movement Registry records permit status.

A genuine warehouse receipt can be the wrong source for usability. A current community update can be the wrong source for another route. A vendor note can contain real dimensions and a hostile instruction in the same file. Judge the source against the exact claim.

## The handoff rule

One step can be correct while the overall conclusion is still wrong, because the next step may require something that the first one did not establish.

- Twelve totes can be scanned while only ten are released.
- Released cargo can fit while the required rack pushes another load over capacity.
- A permit application can be received while the permit remains pending.
- The clinic can be reachable by 16:00 while the gate closes before the truck arrives.

The thread passes only when every required handoff to the decision point passes. Keep later states honest: an estimated clinic arrival is not delivery, and delivery is not yet clinic confirmation.
