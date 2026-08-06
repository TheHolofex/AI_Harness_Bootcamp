import { randomUUID } from "node:crypto";
import { Agent, type AgentTool } from "@earendil-works/pi-agent-core";
import { contentText, createModels } from "@earendil-works/pi-ai";
import { xaiProvider } from "@earendil-works/pi-ai/providers/xai";
import type { Conversation, LabRuntime } from "./types.js";

export class PiRuntime implements LabRuntime {
  private readonly models = createModels();
  private readonly model;

  private constructor(modelId: string) {
    this.models.setProvider(xaiProvider());
    const model = this.models.getModel("xai", modelId);
    if (!model) throw new Error(`Pi does not list xAI model '${modelId}'.`);
    this.model = model;
  }

  static async create(): Promise<PiRuntime> {
    const modelId = process.env.HB_XAI_MODEL?.trim() || "grok-4.5";
    const runtime = new PiRuntime(modelId);
    const auth = await runtime.models.checkAuth("xai");
    if (!auth) throw new Error("XAI_API_KEY is not available in this PowerShell window.");
    return runtime;
  }

  conversation(systemPrompt: string, tools: AgentTool[] = []): Conversation {
    const agent = new Agent({
      initialState: {
        systemPrompt,
        model: this.model,
        thinkingLevel: "low",
        tools,
      },
      streamFn: this.models.streamSimple.bind(this.models),
      sessionId: `pi-pattern-${randomUUID()}`,
    });

    return {
      prompt: async (input: string) => {
        await agent.prompt(input);
        if (agent.state.errorMessage) throw new Error(agent.state.errorMessage);
        const message = [...agent.state.messages]
          .reverse()
          .find((candidate) => candidate.role === "assistant");
        if (!message || message.role !== "assistant") {
          throw new Error("Pi finished without an assistant message.");
        }
        if (message.stopReason === "error" || message.stopReason === "aborted") {
          throw new Error(message.errorMessage || `Pi stopped with ${message.stopReason}.`);
        }
        const text = contentText(message.content).trim();
        if (!text) throw new Error("Pi finished without a text result.");
        return text;
      },
    };
  }

  async ask(systemPrompt: string, input: string): Promise<string> {
    return this.conversation(systemPrompt).prompt(input);
  }
}
