import type { Pattern } from "../types.js";
import { promptChain } from "./01-prompt-chain.js";
import { routing } from "./02-routing.js";
import { parallel } from "./03-parallel.js";
import { orchestratorWorkers } from "./04-orchestrator-workers.js";
import { handoff } from "./05-handoff.js";
import { evaluatorOptimizer } from "./06-evaluator-optimizer.js";
import { toolLoop } from "./07-tool-loop.js";
import { plannerExecutor } from "./08-planner-executor.js";
import { reflection } from "./09-reflection.js";
import { supervisorTools } from "./10-supervisor-tools.js";

export const patterns: Record<string, Pattern> = {
  "01": promptChain,
  "02": routing,
  "03": parallel,
  "04": orchestratorWorkers,
  "05": handoff,
  "06": evaluatorOptimizer,
  "07": toolLoop,
  "08": plannerExecutor,
  "09": reflection,
  "10": supervisorTools,
};
