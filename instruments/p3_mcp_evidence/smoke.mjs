import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import {
  copyFile,
  mkdtemp,
  readFile,
  rm,
  symlink,
  unlink,
  writeFile,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

import { Client } from "@modelcontextprotocol/client";
import { StdioClientTransport } from "@modelcontextprotocol/client/stdio";

import {
  describeServer,
  EvidenceAccessError,
  LIST_TOOL_DESCRIPTION,
  MAX_FILE_BYTES,
  READ_TOOL_DESCRIPTION,
  READ_ONLY_ANNOTATIONS,
  readEvidenceFile,
  SERVER_INSTRUCTIONS,
  SERVER_NAME,
  SERVER_VERSION,
  TOOL_NAMES,
  TRACKS,
  validateEvidenceRoot,
} from "./server.mjs";

const execFileAsync = promisify(execFile);
const moduleDirectory = dirname(fileURLToPath(import.meta.url));
const frozenBriefDirectory = join(moduleDirectory, "..", "p3_frozen_brief");
const serverPath = join(moduleDirectory, "server.mjs");
const skippedSymlinkChecks = [];

function corpusPath(track, filename) {
  return filename === "BRIEF-v1.md"
    ? join(frozenBriefDirectory, filename)
    : join(frozenBriefDirectory, track, "corpus", filename);
}

async function copyTrack(root, track) {
  for (const filename of TRACKS[track]) {
    await copyFile(corpusPath(track, filename), join(root, filename));
  }
}

async function makeTrack(track) {
  const root = await mkdtemp(join(tmpdir(), `p3-mcp-${track}-`));
  await copyTrack(root, track);
  return root;
}

async function expectEvidenceError(action, code) {
  await assert.rejects(action, (error) => {
    assert.ok(error instanceof EvidenceAccessError);
    assert.equal(error.code, code);
    return true;
  });
}

function symlinksUnsupported(error) {
  return ["EACCES", "EPERM", "ENOSYS", "ENOTSUP", "UNKNOWN"].includes(
    error?.code,
  );
}

async function testDescribeMode() {
  const root = await makeTrack("engineering");
  try {
    const runDescribe = () =>
      execFileAsync(process.execPath, [serverPath, root, "--describe"], {
        cwd: root,
        timeout: 5_000,
        windowsHide: true,
      });
    const first = await runDescribe();
    const second = await runDescribe();
    assert.equal(first.stderr, "", "describe: stderr stays clean");
    assert.equal(second.stderr, "", "describe: repeat stderr stays clean");
    assert.equal(first.stdout, second.stdout, "describe: deterministic JSON");

    const description = JSON.parse(first.stdout);
    const validatedRoot = await validateEvidenceRoot(root);
    assert.deepEqual(description, describeServer(validatedRoot));
    assert.deepEqual(description.connection.selfReportedServer, {
      name: SERVER_NAME,
      version: SERVER_VERSION,
      verifiedIdentity: false,
    });
    assert.equal(description.connection.transport, "stdio");
    assert.equal(description.surface.resourceCount, 0);
    assert.equal(description.surface.promptCount, 0);
    assert.deepEqual(
      description.surface.tools.map((tool) => tool.name),
      TOOL_NAMES,
    );
    assert.deepEqual(description.surface.tools[0].inputSchema, {
      $schema: "https://json-schema.org/draft/2020-12/schema",
      type: "object",
      properties: {},
      additionalProperties: false,
    });
    assert.deepEqual(description.surface.tools[1].inputSchema, {
      $schema: "https://json-schema.org/draft/2020-12/schema",
      type: "object",
      properties: {
        filename: {
          type: "string",
          minLength: 1,
          maxLength: 128,
        },
      },
      required: ["filename"],
      additionalProperties: false,
    });
    assert.equal(description.surface.tools[0].description, LIST_TOOL_DESCRIPTION);
    assert.equal(description.surface.tools[1].description, READ_TOOL_DESCRIPTION);
    for (const tool of description.surface.tools) {
      assert.deepEqual(tool.annotations, READ_ONLY_ANNOTATIONS);
      assert.equal(tool.outputSchema.type, "object");
      assert.equal(tool.outputSchema.additionalProperties, false);
    }
    assert.equal(description.serverInstructions, SERVER_INSTRUCTIONS);
    assert.match(description.enforcement.processBoundary, /user's privileges/);
    assert.match(description.enforcement.processBoundary, /no OS-level sandbox/);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
}

async function testTrackValidation() {
  const incomplete = await makeTrack("engineering");
  try {
    await unlink(join(incomplete, "F3_deploy_log.md"));
    await expectEvidenceError(
      () => validateEvidenceRoot(incomplete),
      "invalid_track",
    );
  } finally {
    await rm(incomplete, { recursive: true, force: true });
  }

  const ambiguous = await makeTrack("engineering");
  try {
    await copyTrack(ambiguous, "mission_ops");
    await expectEvidenceError(
      () => validateEvidenceRoot(ambiguous),
      "ambiguous_track",
    );
  } finally {
    await rm(ambiguous, { recursive: true, force: true });
  }
}

async function testFileGuards() {
  const root = await makeTrack("engineering");
  const guardedFilename = "F1_status_page.md";
  const guardedPath = join(root, guardedFilename);
  const originalPath = corpusPath("engineering", guardedFilename);
  try {
    const validatedRoot = await validateEvidenceRoot(root);
    await expectEvidenceError(
      () => readEvidenceFile(validatedRoot, "output_codex.md"),
      "unknown_file",
    );
    await expectEvidenceError(
      () => readEvidenceFile(validatedRoot, "../BRIEF-v1.md"),
      "unknown_file",
    );

    await writeFile(guardedPath, Buffer.alloc(MAX_FILE_BYTES + 1, 0x61));
    await expectEvidenceError(
      () => readEvidenceFile(validatedRoot, guardedFilename),
      "file_too_large",
    );
    await copyFile(originalPath, guardedPath);

    await writeFile(guardedPath, Buffer.from([0xc3, 0x28]));
    await expectEvidenceError(
      () => readEvidenceFile(validatedRoot, guardedFilename),
      "invalid_text",
    );
    await copyFile(originalPath, guardedPath);

    await unlink(guardedPath);
    try {
      await symlink(originalPath, guardedPath, "file");
      await expectEvidenceError(
        () => readEvidenceFile(validatedRoot, guardedFilename),
        "symlink_denied",
      );
    } catch (error) {
      if (!symlinksUnsupported(error)) throw error;
      skippedSymlinkChecks.push(`file symlink (${error.code})`);
    } finally {
      await unlink(guardedPath).catch(() => {});
      await copyFile(originalPath, guardedPath);
    }

    const linkedRoot = `${root}-link`;
    try {
      await symlink(
        root,
        linkedRoot,
        process.platform === "win32" ? "junction" : "dir",
      );
      await expectEvidenceError(
        () => validateEvidenceRoot(linkedRoot),
        "symlink_denied",
      );
    } catch (error) {
      if (!symlinksUnsupported(error)) throw error;
      skippedSymlinkChecks.push(`root symlink (${error.code})`);
    } finally {
      await unlink(linkedRoot).catch(() => {});
    }
  } finally {
    await rm(root, { recursive: true, force: true });
  }
}

async function runProtocolSession({ track, mode }) {
  const root = await makeTrack(track);
  const clientOptions =
    mode === "auto" ? { versionNegotiation: { mode: "auto" } } : undefined;
  const client = new Client(
    { name: `p3-smoke-${mode}`, version: "1.0.0" },
    clientOptions,
  );
  const transport = new StdioClientTransport({
    command: process.execPath,
    args: [serverPath, root],
    cwd: root,
    stderr: "pipe",
  });
  let serverErrors = "";
  transport.stderr?.on("data", (chunk) => {
    serverErrors += chunk.toString();
  });

  try {
    await client.connect(transport);
    const capabilities = client.getServerCapabilities() ?? {};
    assert.equal(capabilities.resources, undefined, `${mode}: no resources`);
    assert.equal(capabilities.prompts, undefined, `${mode}: no prompts`);
    assert.equal(client.getInstructions(), SERVER_INSTRUCTIONS);

    const originalDebug = console.debug;
    console.debug = () => {};
    try {
      const { resources } = await client.listResources();
      const { prompts } = await client.listPrompts();
      assert.deepEqual(resources, [], `${mode}: empty resource list`);
      assert.deepEqual(prompts, [], `${mode}: empty prompt list`);
    } finally {
      console.debug = originalDebug;
    }

    const { tools } = await client.listTools();
    const describedTools = describeServer(await validateEvidenceRoot(root)).surface.tools;
    assert.deepEqual(
      tools.map((tool) => tool.name),
      TOOL_NAMES,
      `${mode}: exact tool surface`,
    );
    for (const [index, tool] of tools.entries()) {
      const describedTool = describedTools[index];
      assert.equal(tool.title, describedTool.title, `${mode}: title matches describe`);
      assert.equal(
        tool.description,
        describedTool.description,
        `${mode}: description matches describe`,
      );
      assert.deepEqual(
        tool.inputSchema,
        describedTool.inputSchema,
        `${mode}: input schema matches describe`,
      );
      assert.deepEqual(
        tool.outputSchema,
        describedTool.outputSchema,
        `${mode}: output schema matches describe`,
      );
      assert.deepEqual(
        tool.annotations,
        describedTool.annotations,
        `${mode}: annotations match describe`,
      );
      assert.equal(
        tool.inputSchema.additionalProperties,
        false,
        `${mode}: strict input schema for ${tool.name}`,
      );
      assert.equal(
        tool.outputSchema?.additionalProperties,
        false,
        `${mode}: strict output schema for ${tool.name}`,
      );
    }

    const listed = await client.callTool({
      name: TOOL_NAMES[0],
      arguments: {},
    });
    assert.equal(listed.isError, undefined, `${mode}: list succeeds`);
    assert.equal(listed.structuredContent.track, track, `${mode}: track identity`);
    assert.deepEqual(
      listed.structuredContent.files.map((file) => file.filename),
      TRACKS[track],
      `${mode}: deterministic file list`,
    );

    const expectedBuffer = await readFile(join(root, "BRIEF-v1.md"));
    const expectedHash = createHash("sha256")
      .update(expectedBuffer)
      .digest("hex");
    const read = await client.callTool({
      name: TOOL_NAMES[1],
      arguments: { filename: "BRIEF-v1.md" },
    });
    assert.equal(read.isError, undefined, `${mode}: allowed read succeeds`);
    assert.equal(read.structuredContent.filename, "BRIEF-v1.md");
    assert.equal(read.structuredContent.bytes, expectedBuffer.byteLength);
    assert.equal(read.structuredContent.sha256, expectedHash);
    assert.equal(read.structuredContent.content, expectedBuffer.toString("utf8"));

    for (const filename of ["../BRIEF-v1.md", "output_codex.md"]) {
      const denied = await client.callTool({
        name: TOOL_NAMES[1],
        arguments: { filename },
      });
      assert.equal(denied.isError, true, `${mode}: ${filename} is denied`);
      assert.equal(denied.structuredContent.error, "unknown_file");
      assert.match(denied.content[0].text, /Read denied/);
      assert.deepEqual(denied.structuredContent.allowedFiles, TRACKS[track]);
    }
  } finally {
    await client.close().catch(() => {});
    await rm(root, { recursive: true, force: true });
  }

  assert.equal(serverErrors, "", `${mode}: server stderr must stay clean`);
}

await testDescribeMode();
await testTrackValidation();
await testFileGuards();
await runProtocolSession({ track: "engineering", mode: "auto" });
await runProtocolSession({ track: "mission_ops", mode: "legacy" });

const skipNote =
  skippedSymlinkChecks.length === 0
    ? "all symlink guards exercised"
    : `symlink checks skipped where unsupported: ${skippedSymlinkChecks.join(", ")}`;
console.log(
  `P3 MCP smoke passed: describe, guards, modern auto, and legacy stdio; ${skipNote}.`,
);
