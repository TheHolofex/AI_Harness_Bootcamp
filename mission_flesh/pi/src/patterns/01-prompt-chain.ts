import type { Pattern } from "../types.js";
import { compact } from "../types.js";

export const promptChain: Pattern = async (lab) => {
  const source = "Shipment 184 is due Friday. The supplier moved dispatch to Saturday. Assembly has six hours of buffer and the customer demo is Monday at 09:00.";
  const facts = await lab.ask(
    "Extract only dated facts and quantities. Return one compact sentence.",
    source,
  );
  const decision = await lab.ask(
    "Turn supplied facts into one operational decision. Return one sentence.",
    facts,
  );
  const brief = await lab.ask(
    "Write a two-sentence operator brief: situation, then action.",
    decision,
  );

  return {
    id: "01",
    slug: "prompt-chain",
    title: "Prompt chain",
    trace: ["source -> extractor", "extractor -> decision agent", "decision agent -> brief writer"],
    output: compact(brief),
  };
};
