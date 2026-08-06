import assert from "node:assert/strict";
import test from "node:test";
import type { AgentTool } from "@earendil-works/pi-agent-core";
import { patterns } from "../src/patterns/index.js";
import type { Conversation, LabRuntime } from "../src/types.js";

class FakeRuntime implements LabRuntime {
  async ask(systemPrompt: string, input: string): Promise<string> {
    if (/exactly one word/i.test(systemPrompt)) return "billing";
    if (/evaluate/i.test(systemPrompt)) return "REVISE: name the owner and checkpoint.";
    return `result for ${systemPrompt.slice(0, 48)} | ${input.slice(0, 48)}`;
  }

  conversation(systemPrompt: string, tools: AgentTool[] = []): Conversation {
    const history: string[] = [];
    return {
      prompt: async (input: string) => {
        history.push(input);
        for (const tool of tools) {
          await tool.execute(`fake-${tool.name}`, {}, undefined, undefined);
        }
        return `conversation ${history.length} for ${systemPrompt.slice(0, 42)}`;
      },
    };
  }
}

test("all ten pattern implementations complete with observable traces", async () => {
  const ids = Object.keys(patterns).sort();
  assert.deepEqual(ids, ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]);

  for (const id of ids) {
    const result = await patterns[id]?.(new FakeRuntime());
    assert.ok(result, `missing result for ${id}`);
    assert.equal(result.id, id);
    assert.ok(result.title.length > 0);
    assert.ok(result.trace.length >= 2, `${id} has no visible control-flow trace`);
    assert.ok(result.output.length > 0, `${id} has no output`);
  }
});

test("routing rejects output outside its two declared routes", async () => {
  class MalformedRouterRuntime extends FakeRuntime {
    async ask(systemPrompt: string, input: string): Promise<string> {
      if (/exactly one word/i.test(systemPrompt)) return "billing request";
      return super.ask(systemPrompt, input);
    }
  }

  const pattern = patterns["02"];
  assert.ok(pattern);
  await assert.rejects(
    () => pattern(new MalformedRouterRuntime()),
    /unexpected route 'billing request'/,
  );
});

test("evaluator PASS still reaches the optimizer", async () => {
  class PassingEvaluatorRuntime extends FakeRuntime {
    optimizerCalls = 0;

    async ask(systemPrompt: string, input: string): Promise<string> {
      if (/^Evaluate the draft/i.test(systemPrompt)) return "PASS: all fields are present.";
      if (/You are the optimizer/i.test(systemPrompt)) {
        this.optimizerCalls += 1;
        return "Status delayed; impact one day; owner Logistics; checkpoint 14:00Z.";
      }
      return super.ask(systemPrompt, input);
    }
  }

  const runtime = new PassingEvaluatorRuntime();
  const result = await patterns["06"]?.(runtime);
  assert.ok(result);
  assert.equal(runtime.optimizerCalls, 1);
});

test("supervisor cannot satisfy both delegations by repeating one tool", async () => {
  class DuplicateSupervisorRuntime extends FakeRuntime {
    conversation(_systemPrompt: string, tools: AgentTool[] = []): Conversation {
      return {
        prompt: async () => {
          const first = tools[0];
          assert.ok(first);
          await first.execute("duplicate-1", {}, undefined, undefined);
          await first.execute("duplicate-2", {}, undefined, undefined);
          return "decision from one repeated specialty";
        },
      };
    }
  }

  const pattern = patterns["10"];
  assert.ok(pattern);
  await assert.rejects(
    () => pattern(new DuplicateSupervisorRuntime()),
    /both distinct subagent tools/,
  );
});
