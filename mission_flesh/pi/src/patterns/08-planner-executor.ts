import type { Pattern } from "../types.js";
import { compact } from "../types.js";

export const plannerExecutor: Pattern = async (lab) => {
  const goal = "Move the weekly service review from raw tickets to a director-ready three-line decision brief.";
  const plan = await lab.ask(
    "Create exactly three ordered execution steps for the goal. Keep each step to one line.",
    goal,
  );
  let state = "No work completed yet.";
  for (const step of [1, 2, 3]) {
    state = await lab.ask(
      `You are the executor. Perform step ${step} of the supplied plan using the current state. Return the updated state in at most three sentences.`,
      `Goal: ${goal}\nPlan:\n${plan}\nCurrent state:\n${state}`,
    );
  }

  return {
    id: "08",
    slug: "planner-executor",
    title: "Planner and executor",
    trace: ["goal -> planner", "plan step 1 -> executor", "plan step 2 -> executor", "plan step 3 -> executor"],
    output: compact(state),
  };
};
