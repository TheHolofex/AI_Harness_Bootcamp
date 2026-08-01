# Resource handout authoring contract

This file is an internal production contract. It is not published to learners.

## Canonical ownership

The owning block or pre-work page owns the concept's canonical statement. A resource starts where that page ends. It may add a case, instrument, practice method, evidence structure, failure analysis, or transfer move. It may not paraphrase the block page into a second canonical lesson.

Before drafting:

1. Read the full live owning learner page at the catalog's `canonical.path` and fragment.
2. Read the resource entry in `resources/catalog.json` and scope contract in `resources/scopes.json`.
3. Use the catalog path for current course facts and the scope's `canonicalOwner` for topic boundaries or exact working-file wording.
4. Name the novel learner action and inspectable artifact.
5. Check collision IDs before deciding what belongs here.

When a tool fact matters, link to the owning block page. Teach the durable mechanism in the handout. The live owning HTML page wins over prior knowledge, web recollection, model belief, and superseded repository notes when current course facts conflict.

## Required learning arc

Every normal handout must contain these learner-visible moves in a natural sequence:

1. **Orientation:** the situation in which this resource earns attention, the time required, and the artifact the learner will leave with.
2. **Operational model:** a mechanism-level explanation beyond the block page, with defined terms at first use.
3. **Worked case:** a fresh, realistic case followed far enough that the learner can inspect intermediate decisions—not only the polished result.
4. **Failure injection:** a deliberate break, the observable symptom, a diagnosis path, and recovery.
5. **Guided practice:** a bounded exercise with supplied inputs, decision points, and stop conditions.
6. **Evidence artifact:** a copyable table, record, protocol, worksheet, or decision note that proves the learner did the cognitive work.
7. **Self-check:** discriminating questions or predict-before-reveal checks. Model self-assessment and “looks good” never count.
8. **Desk transfer:** a small move the learner can run on a real work item, including a boundary and a return-to-human condition.
9. **Sources:** primary research, standards, or authoritative documentation close to the claims they support, with a short curated source shelf at the end.

PC-1 is the deliberate exception: it is a one-page retrieval aid, not a miniature essay. Its evidence is correct recall and use under work pressure.

## Voice and audience

Write as a calm expert standing beside a capable operator at the keyboard. Put purpose before procedure and the map before the territory. Use complete sentences. Define jargon in the breath where it first matters. Pair every likely failure with a recovery path.

Reject:

- hype, productivity slogans, or tool fandom;
- cold expert walls, glossary dumps, or unexplained notation;
- “you don't need to understand this”;
- vague assurances that nothing can go wrong;
- decorative exercises with no inspectable result;
- first-person production narration;
- making-of language such as “this handout covers,” “in this resource,” “we chose,” “the learning objective,” or design rationale;
- internal terms such as canonical owner, scope rail, collision ID, production wave, reviewer, draft status, or generated page.

Use the application's course vocabulary: project, chat, worktree, permission mode, and subagent. Do not call a chat a thread.

## Figures

Normal handouts require exactly three purposeful figure specifications unless the catalog explicitly grants an exception. A figure must do cognitive work that prose would do poorly: expose a mapping, comparison, dependency, decision, sequence, boundary, or state change.

Every figure needs:

- a short title;
- a concise accessible description;
- a visible caption stating the reading move;
- a text transcript that preserves all important relationships;
- labels that remain useful without color;
- fresh examples that do not expose course mission answers.

Use the existing paper/field SVG grammar and palette. Never use image generation for this resource collection.

## Truth and safety rails

- Do not hardcode model IDs, current product behavior, commands, install steps, versions, provider feature availability, or pricing. Link to the owning block/pre-work page where current tool specifics live.
- Never name, quote, count, encode, silhouette, or otherwise hint at which P5 intake items are poisoned. The rule applies to prose, exercises, filenames, links, captions, alt text, figure labels, descriptions, and metadata. Use entirely fresh cases.
- Do not read or cite facilitator keys, answer keys, cohort pins, or staff-only material.
- Do not link learner pages to facilitator notes, lead runbooks, answer keys, or staff pin sheets.
- Treat external sources as support, not authority transfer. Explain the operational consequence in original words and keep quotations short.

## Resource-agent review loop

The resource author owns one body fragment and one figure-spec file. It does not edit shared catalog, CSS, navigation, templates, block pages, or generated output.

Before reporting completion, the author must spawn an independent read-only review agent. The reviewer checks:

- separation from the canonical block page and collision resources;
- complete learning arc and genuine desk value;
- accuracy and source support;
- cognitive load, voice, and recovery paths;
- exercise answerability and artifact inspectability;
- figure accuracy and accessibility;
- tool-drift, staff-leak, making-of, and P5 spoiler rails.

The author then addresses every finding or records a concrete reason it does not apply, reruns the available source checks, and reports the files changed plus reviewer verdict.
