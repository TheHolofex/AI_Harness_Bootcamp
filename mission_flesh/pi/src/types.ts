import type { AgentTool } from "@earendil-works/pi-agent-core";

export interface Conversation {
  prompt(input: string): Promise<string>;
}

export interface LabRuntime {
  ask(systemPrompt: string, input: string): Promise<string>;
  conversation(systemPrompt: string, tools?: AgentTool[]): Conversation;
}

export interface PatternResult {
  id: string;
  slug: string;
  title: string;
  trace: string[];
  output: string;
}

export type Pattern = (lab: LabRuntime) => Promise<PatternResult>;

export function compact(text: string, limit = 900): string {
  const normalized = text.replace(/\s+/g, " ").trim();
  if (!normalized) throw new Error("A Pi agent returned no text.");
  return normalized.length > limit ? `${normalized.slice(0, limit - 1)}…` : normalized;
}
