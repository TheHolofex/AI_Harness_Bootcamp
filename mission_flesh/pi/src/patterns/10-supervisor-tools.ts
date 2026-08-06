import type { AgentTool } from "@earendil-works/pi-agent-core";
import { Type } from "@earendil-works/pi-ai";
import type { Pattern } from "../types.js";
import { compact } from "../types.js";

export const supervisorTools: Pattern = async (lab) => {
  const delegations: string[] = [];

  const childTool = (name: string, specialty: string): AgentTool => ({
    name,
    label: `Ask ${specialty}`,
    description: `Delegate one focused assessment to the ${specialty} subagent.`,
    parameters: Type.Object({}),
    async execute() {
      delegations.push(specialty);
      const answer = await lab.ask(
        `You are the ${specialty} subagent. Return one finding and one recommendation.`,
        "A supplier outage threatens tomorrow's customer migration; a manual workaround can cover half the volume.",
      );
      return {
        content: [{ type: "text", text: answer }],
        details: { specialty },
      };
    },
  });

  const tools = [
    childTool("ask_operations", "operations"),
    childTool("ask_customer", "customer"),
  ];
  const supervisor = lab.conversation(
    "You are the supervisor. Call both subagent tools, compare their returns, and issue one decision with one reason.",
    tools,
  );
  const answer = await supervisor.prompt("Decide how to handle tomorrow's migration. Call ask_operations and ask_customer before answering.");
  const distinctDelegations = new Set(delegations);
  if (!distinctDelegations.has("operations") || !distinctDelegations.has("customer")) {
    throw new Error("The supervisor did not call both distinct subagent tools.");
  }

  return {
    id: "10",
    slug: "supervisor-tools",
    title: "Supervisor with subagents as tools",
    trace: ["goal -> supervisor", "supervisor -> operations and customer subagent tools", "subagent returns -> supervisor decision"],
    output: compact(answer),
  };
};
