import type { Pattern } from "../types.js";
import { compact } from "../types.js";

export const orchestratorWorkers: Pattern = async (lab) => {
  const goal = "Prepare a 10:00 launch-readiness picture from product, support, and infrastructure evidence.";
  const plan = await lab.ask(
    "Act as an orchestrator. Assign distinct work to product, support, and infrastructure workers. Use three short lines.",
    goal,
  );
  const workers = ["product", "support", "infrastructure"] as const;
  const returns = await Promise.all(
    workers.map((worker) => lab.ask(
      `You are the ${worker} worker. Complete only your assigned slice and return one finding plus one recommendation.`,
      `Goal: ${goal}\nOrchestrator plan:\n${plan}`,
    )),
  );
  const synthesis = await lab.ask(
    "You are the orchestrator. Reconcile the worker returns into a launch, hold, or conditional-launch decision with one reason.",
    returns.map((text, index) => `${workers[index]}: ${text}`).join("\n"),
  );

  return {
    id: "04",
    slug: "orchestrator-workers",
    title: "Orchestrator and workers",
    trace: ["goal -> orchestrator plan", "plan -> three scoped workers", "worker returns -> orchestrator synthesis"],
    output: compact(synthesis),
  };
};
