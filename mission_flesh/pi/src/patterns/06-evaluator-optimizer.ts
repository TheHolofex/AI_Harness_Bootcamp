import type { Pattern } from "../types.js";
import { compact } from "../types.js";

export const evaluatorOptimizer: Pattern = async (lab) => {
  const task = "Write a status note for a delayed warehouse cutover. It must name status, impact, owner, and next checkpoint.";
  const draft = await lab.ask("Write the requested status note in at most four sentences.", task);
  const evaluation = await lab.ask(
    "Evaluate the draft against status, impact, owner, and next checkpoint. Return PASS or REVISE followed by one sentence.",
    draft,
  );
  const optimized = await lab.ask(
    "You are the optimizer. Use the evaluator verdict to return the final note. If it says PASS, preserve the draft. If it says REVISE, rewrite once to satisfy the named gap. Return only the final note.",
    `Task: ${task}\nDraft: ${draft}\nEvaluation: ${evaluation}`,
  );

  return {
    id: "06",
    slug: "evaluator-optimizer",
    title: "Evaluator and optimizer",
    trace: ["task -> generator", "draft -> evaluator", "evaluation -> optimizer"],
    output: compact(optimized),
  };
};
