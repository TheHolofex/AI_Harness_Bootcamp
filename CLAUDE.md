# AI Harness Bootcamp — authoring rules

Constraints for anyone (human or AI) creating or revising course content in this repository.

## Course progression rule

Every project assumes learners can already do everything required in the earlier projects. Earlier capabilities may return as prerequisites, operating constraints, or evidence standards, but they are not new learning objectives and must not be retaught as though the class is seeing them for the first time. Give a short reminder or link back at the point of use; reserve project time for the next capability.

Write each project's mastery claim and objectives by answering:

> **What can the learner now do that they could not do before this project?**

Apply these tests whenever a project is created or revised:

1. **Capability-delta test:** complete the sentence "Before this project, the learner could ___. After this project, the learner can ___." The second clause must name a meaningful new capability, not a new file, tool, scenario, or repetition count.
2. **Prerequisite test:** if an earlier project already taught the skill, state it as assumed knowledge or a required quality bar. Do not count it again as an objective.
3. **Dependency test:** each new objective must use at least one earlier capability and extend it into work the learner could not previously perform.
4. **Evidence test:** files, installations, checkboxes, logs, reflections, and transfer entries may prove or reinforce learning. They are not objectives by themselves.
5. **Progression test:** the mastery claim must add one clear capability to the course arc without restating an earlier mastery claim in different words.

Applied to `operator/CAPABILITIES.md`: an earlier skill may stay in a project's requirements as a prerequisite, but repeating it does not earn the new capability. If a requirement could move unchanged to an earlier project, it is not a new objective — state it as assumed knowledge, or rewrite it around what this project adds.

Remediation is the exception. If learners cannot perform a prerequisite, repair it explicitly as prerequisite recovery without redefining it as the current project's new content.

## Learner-facing content

Never ship the making-of frame. Course pages, handouts, and briefs teach the craft, not the curriculum. No design rationale (why content is sequenced this way, why a mechanism belongs to one party, why a topic was scoped in or out) and no meta-commentary about the artifact ("what we'll cover," "in this section," section recaps, handoffs to companion materials).

Test: would this still exist if the same knowledge were delivered by a book, a mentor, or on the job — with no course around it? If it only makes sense because there is an artifact, cut it, or reframe it so it survives outside the setting.

Put this constraint in the brief of any subagent or generator writing learner-facing prose, and check the output against the test before delivery.

## Repository shape

The website is the course. Do not add learner-facing Markdown pages — core instruction goes in the owning pre-work or module HTML page, optional depth goes through the resource build system, and a raw file is added only when working with that file is part of the exercise. See [`README.md`](README.md) for the path map.
