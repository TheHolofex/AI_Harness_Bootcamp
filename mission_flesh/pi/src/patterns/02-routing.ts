import type { Pattern } from "../types.js";
import { compact } from "../types.js";

export const routing: Pattern = async (lab) => {
  const request = "The customer was charged twice for invoice 771 and wants the duplicate reversed.";
  const routeText = await lab.ask(
    "Classify the request. Return exactly one word: billing or technical.",
    request,
  );
  const route = routeText.trim().toLowerCase();
  if (route !== "billing" && route !== "technical") {
    throw new Error(`Router returned unexpected route '${routeText.trim()}'.`);
  }
  const systemPrompt = route === "billing"
    ? "You are the billing specialist. Give the next action and required record in two sentences."
    : "You are the technical specialist. Give one diagnostic and one next action in two sentences.";
  const answer = await lab.ask(systemPrompt, request);

  return {
    id: "02",
    slug: "routing",
    title: "Routing",
    trace: [`request -> router (${route})`, `${route} route -> ${route} specialist`],
    output: compact(answer),
  };
};
