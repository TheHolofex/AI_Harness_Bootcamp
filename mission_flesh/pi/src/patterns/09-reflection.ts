import type { Pattern } from "../types.js";
import { compact } from "../types.js";

export const reflection: Pattern = async (lab) => {
  const agent = lab.conversation(
    "Write concise operational prose. When asked to reflect, inspect your immediately preceding answer and replace it with a stronger version.",
  );
  const draft = await agent.prompt(
    "Draft a two-sentence note explaining that the release is ready but the rollback owner is not named.",
  );
  const revised = await agent.prompt(
    "Reflect on your draft. Make the missing ownership explicit, remove any vague language, and return only the revised two-sentence note.",
  );

  return {
    id: "09",
    slug: "reflection",
    title: "Reflection",
    trace: ["task -> stateful agent draft", "same transcript -> self-critique and revision"],
    output: compact(`${revised}\n(previous draft: ${compact(draft, 220)})`),
  };
};
