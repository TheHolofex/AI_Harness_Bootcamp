import type { Pattern } from "../types.js";
import { compact } from "../types.js";

export const handoff: Pattern = async (lab) => {
  const request = "A strategic customer says the renewal quote excludes the support tier promised in the signed order form.";
  const transfer = await lab.ask(
    "You own intake. Produce a bounded handoff with issue, evidence needed, and receiving specialty. Three lines only.",
    request,
  );
  const resolution = await lab.ask(
    "You now own commercial resolution. Use only the handoff. State the first two actions and the decision owner.",
    transfer,
  );

  return {
    id: "05",
    slug: "handoff",
    title: "Handoff",
    trace: ["request -> intake owner", "handoff artifact -> commercial owner"],
    output: compact(resolution),
  };
};
