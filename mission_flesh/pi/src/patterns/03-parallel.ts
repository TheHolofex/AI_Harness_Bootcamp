import type { Pattern } from "../types.js";
import { compact } from "../types.js";

export const parallel: Pattern = async (lab) => {
  const incident = "Checkout latency rose from 400 ms to 4.8 s after release 58. Error rate is 7%. A campaign starts in 45 minutes.";
  const lenses = [
    ["operations", "Assess immediate operational impact in one sentence."],
    ["customer", "Assess customer impact in one sentence."],
    ["release", "Assess the release decision in one sentence."],
  ] as const;
  const findings = await Promise.all(
    lenses.map(([name, instruction]) => lab.ask(`You are the ${name} analyst. ${instruction}`, incident)),
  );
  const synthesis = await lab.ask(
    "Merge three independent findings into one three-sentence incident direction.",
    findings.map((text, index) => `${lenses[index]?.[0]}: ${text}`).join("\n"),
  );

  return {
    id: "03",
    slug: "parallel",
    title: "Parallel fan-out and fan-in",
    trace: ["incident -> operations | customer | release", "three parallel returns -> synthesizer"],
    output: compact(synthesis),
  };
};
