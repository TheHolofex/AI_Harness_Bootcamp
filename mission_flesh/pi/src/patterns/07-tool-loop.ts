import type { AgentTool } from "@earendil-works/pi-agent-core";
import { Type } from "@earendil-works/pi-ai";
import type { Pattern } from "../types.js";
import { compact } from "../types.js";

export const toolLoop: Pattern = async (lab) => {
  let lookups = 0;
  const lookupTicket: AgentTool = {
    name: "lookup_ticket",
    label: "Lookup ticket",
    description: "Return the current record for incident INC-204.",
    parameters: Type.Object({}),
    async execute() {
      lookups += 1;
      return {
        content: [{ type: "text", text: "INC-204 owner=Platform status=Mitigating next=09:30Z" }],
        details: { ticket: "INC-204" },
      };
    },
  };
  const agent = lab.conversation(
    "Use the available tool to answer the request. After observing the result, return owner, status, and next checkpoint in one sentence.",
    [lookupTicket],
  );
  const answer = await agent.prompt("Look up INC-204 and report its current state. You must call lookup_ticket first.");
  if (lookups < 1) throw new Error("The tool-using agent did not call lookup_ticket.");

  return {
    id: "07",
    slug: "tool-loop",
    title: "Tool-using agent loop",
    trace: ["request -> agent", `agent -> lookup_ticket (${lookups} call${lookups === 1 ? "" : "s"})`, "tool observation -> agent answer"],
    output: compact(answer),
  };
};
