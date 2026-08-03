import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import {
  appendFile,
  copyFile,
  cp,
  lstat,
  mkdtemp,
  readFile,
  rm,
  symlink,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

import { Client } from "@modelcontextprotocol/client";
import { StdioClientTransport } from "@modelcontextprotocol/client/stdio";

import {
  READ_ONLY_ANNOTATIONS,
  SERVER_INSTRUCTIONS,
  TOOL_NAMES,
} from "../mcp/server.mjs";


const execFileAsync = promisify(execFile);
const testsDirectory = dirname(fileURLToPath(import.meta.url));
const pluginDirectory = resolve(testsDirectory, "..");
const referenceDirectory = resolve(pluginDirectory, "..", "..");
const starterDirectory = resolve(referenceDirectory, "..", "starter");
const serverPath = join(pluginDirectory, "mcp", "server.mjs");

async function resolvePython() {
  const candidates = process.env.PROJECT_ORGANIZER_TEST_PYTHON
    ? [process.env.PROJECT_ORGANIZER_TEST_PYTHON]
    : process.platform === "win32"
      ? ["python", "py"]
      : ["python3", "python"];
  for (const command of candidates) {
    try {
      const args = command === "py" ? ["-3", "-c", "import os,sys;print(os.path.abspath(sys.executable))"] : ["-c", "import os,sys;print(os.path.abspath(sys.executable))"];
      const { stdout } = await execFileAsync(command, args, { timeout: 5_000, windowsHide: true });
      const value = stdout.trim().split(/\r?\n/).at(-1);
      if (value) return value;
    } catch {
      // Try the next normal Python launcher.
    }
  }
  throw new Error("Python 3 interpreter not found for Project Organizer smoke test");
}

const python = await resolvePython();

async function makeProject() {
  const root = await mkdtemp(join(tmpdir(), "p2-project-organizer-"));
  await cp(starterDirectory, root, { recursive: true, force: false });
  for (const filename of ["schema.sql", "build_project_ledger.py", "verify_project_ledger.py"]) {
    await copyFile(join(referenceDirectory, filename), join(root, filename));
  }
  const build = await execFileAsync(
    python,
    [join(root, "build_project_ledger.py"), "--project-root", root],
    { cwd: root, timeout: 10_000, windowsHide: true },
  );
  assert.match(build.stdout, /Built project_ledger\.sqlite3/);
  assert.equal(build.stderr, "");
  return root;
}

async function sha256(path) {
  return createHash("sha256").update(await readFile(path)).digest("hex");
}

async function protocolRun(root, mode) {
  const client = new Client(
    { name: `project-organizer-smoke-${mode}`, version: "1.0.0" },
    mode === "auto" ? { versionNegotiation: { mode: "auto" } } : undefined,
  );
  const transport = new StdioClientTransport({
    command: process.execPath,
    args: [serverPath, root],
    cwd: root,
    env: { ...process.env, PROJECT_ORGANIZER_PYTHON: python },
    stderr: "pipe",
  });
  let serverErrors = "";
  transport.stderr?.on("data", (chunk) => {
    serverErrors += chunk.toString();
  });
  const databasePath = join(root, "project_ledger.sqlite3");
  const beforeHash = await sha256(databasePath);
  const beforeInfo = await lstat(databasePath);
  try {
    await client.connect(transport);
    assert.equal(client.getInstructions(), SERVER_INSTRUCTIONS);
    const capabilities = client.getServerCapabilities() ?? {};
    assert.equal(capabilities.resources, undefined);
    assert.equal(capabilities.prompts, undefined);
    const { tools } = await client.listTools();
    assert.deepEqual(tools.map((tool) => tool.name), TOOL_NAMES);
    for (const tool of tools) {
      assert.deepEqual(tool.annotations, READ_ONLY_ANNOTATIONS);
      assert.equal(tool.inputSchema.type, "object");
      assert.equal(tool.inputSchema.additionalProperties, false);
      assert.equal(tool.outputSchema?.type, "object");
      assert.equal(tool.outputSchema?.additionalProperties, false);
    }

    const snapshot = await client.callTool({ name: "get_project_snapshot", arguments: {} });
    assert.equal(snapshot.isError, undefined);
    assert.equal(snapshot.structuredContent.project.project_id, "PRJ-001");
    assert.equal(snapshot.structuredContent.counts.deliverables, 4);
    assert.equal(snapshot.structuredContent.counts.unknowns, 1);
    assert.equal("critical_dependency_path" in snapshot.structuredContent, false);
    assert.equal("blocked_work" in snapshot.structuredContent, false);
    assert.equal("decision_queue" in snapshot.structuredContent, false);
    assert.match(snapshot.structuredContent.next.source_id, /^SRC-\d{3}$/);
    assert.deepEqual(snapshot.structuredContent.unknowns, [{
      field: "DEC-002.decision_owner",
      value: "Not assigned in source",
      impact: "DLV-004 cannot state a defensible GO or HOLD rule, and the sponsor review may slip.",
      needed_by: "2026-08-10",
      source_id: "SRC-004",
    }]);

    const ready = await client.callTool({ name: "get_ready_work", arguments: {} });
    assert.equal(ready.structuredContent.count, 1);
    assert.equal(ready.structuredContent.ready_work[0].deliverable_id, "DLV-002");
    assert.deepEqual(ready.structuredContent.ready_work[0].readiness_evidence, [{
      dependency_id: "DEP-001",
      predecessor_deliverable_id: "DLV-001",
      predecessor_status: "complete",
      dependency_source_id: "SRC-003",
      predecessor_source_id: "SRC-002",
    }]);
    assert.equal(ready.structuredContent.source_fingerprint, snapshot.structuredContent.source_fingerprint);

    const dependency = await client.callTool({
      name: "get_dependency_path",
      arguments: { deliverable_id: "DLV-004" },
    });
    assert.deepEqual(
      dependency.structuredContent.launch_path.map((item) => item.deliverable_id),
      ["DLV-001", "DLV-002", "DLV-003", "DLV-004"],
    );
    assert.equal(dependency.structuredContent.source_fingerprint, snapshot.structuredContent.source_fingerprint);

    const decisions = await client.callTool({
      name: "get_decision_queue",
      arguments: { limit: 10 },
    });
    assert.equal(decisions.structuredContent.count, 2);
    assert.equal(decisions.structuredContent.decisions[1].decision_owner, "Not assigned in source");
    assert.equal(decisions.structuredContent.source_fingerprint, snapshot.structuredContent.source_fingerprint);

    const denied = await client.callTool({
      name: "get_dependency_path",
      arguments: { deliverable_id: "DLV-999" },
    });
    assert.equal(denied.isError, true);
    assert.match(denied.content[0].text, /Unknown deliverable_id/);
  } finally {
    await client.close().catch(() => {});
  }
  assert.equal(serverErrors, "");
  assert.equal(await sha256(databasePath), beforeHash, `${mode}: tool calls cannot change database bytes`);
  assert.equal((await lstat(databasePath)).mtimeMs, beforeInfo.mtimeMs, `${mode}: tool calls cannot touch database mtime`);
}

async function expectSnapshotError(root, pattern) {
  const client = new Client({ name: "project-organizer-negative", version: "1.0.0" });
  const transport = new StdioClientTransport({
    command: process.execPath,
    args: [serverPath, root],
    cwd: root,
    env: { ...process.env, PROJECT_ORGANIZER_PYTHON: python },
    stderr: "pipe",
  });
  try {
    await client.connect(transport);
    const result = await client.callTool({ name: "get_project_snapshot", arguments: {} });
    assert.equal(result.isError, true);
    assert.match(result.content[0].text, pattern);
  } finally {
    await client.close().catch(() => {});
  }
}

async function testDescribeAndFreshness(root) {
  const env = { ...process.env, PROJECT_ORGANIZER_PYTHON: python };
  const first = await execFileAsync(process.execPath, [serverPath, root, "--describe"], {
    cwd: root, env, timeout: 10_000, windowsHide: true,
  });
  const second = await execFileAsync(process.execPath, [serverPath, root, "--describe"], {
    cwd: root, env, timeout: 10_000, windowsHide: true,
  });
  assert.equal(first.stdout, second.stdout);
  const description = JSON.parse(first.stdout);
  assert.deepEqual(description.tools, TOOL_NAMES);
  assert.deepEqual(description.capabilities, { resources: 0, prompts: 0, writeTools: 0, network: false });

  const sourcePath = join(root, "source_packet", "01_project_charter.md");
  await appendFile(sourcePath, "\nSource-side note added after the ledger build.\n", "utf8");
  await expectSnapshotError(root, /Ledger\/source verification failed|values differ|Source hash changed/);
  await assert.rejects(
    execFileAsync(python, [join(root, "verify_project_ledger.py"), "--project-root", root], {
      cwd: root, timeout: 10_000, windowsHide: true,
    }),
    (error) => /Source hash changed after build/.test(error.stdout),
  );
  await execFileAsync(
    python,
    [join(root, "build_project_ledger.py"), "--project-root", root, "--rebuild"],
    { cwd: root, timeout: 10_000, windowsHide: true },
  );
  const verified = await execFileAsync(
    python,
    [join(root, "verify_project_ledger.py"), "--project-root", root],
    { cwd: root, timeout: 10_000, windowsHide: true },
  );
  assert.match(verified.stdout, /^PASS project ledger:/);
}

async function testDependencyContradiction(root) {
  const database = join(root, "project_ledger.sqlite3");
  const mutation = [
    "import sqlite3,sys",
    "con=sqlite3.connect(sys.argv[1])",
    "con.execute(\"UPDATE dependencies SET status='satisfied' WHERE dependency_id='DEP-002'\")",
    "con.commit()",
    "con.close()",
  ].join(";");
  await execFileAsync(python, ["-c", mutation, database], { cwd: root, timeout: 5_000, windowsHide: true });
  await assert.rejects(
    execFileAsync(python, [join(root, "verify_project_ledger.py"), "--project-root", root], {
      cwd: root, timeout: 10_000, windowsHide: true,
    }),
    (error) => /dependencies values differ from the current source packet|DEP-002 status contradicts predecessor status/.test(error.stdout),
  );
  await expectSnapshotError(root, /dependencies values differ from the current source packet|DEP-002 status contradicts predecessor status/);
}

async function testRootSymlinkRejected(root) {
  const link = `${root}-link`;
  try {
    await symlink(root, link, process.platform === "win32" ? "junction" : "dir");
  } catch (error) {
    if (["EACCES", "EPERM", "ENOSYS", "ENOTSUP"].includes(error?.code)) return;
    throw error;
  }
  try {
    await assert.rejects(
      execFileAsync(process.execPath, [serverPath, link, "--validate-only"], {
        cwd: root,
        env: { ...process.env, PROJECT_ORGANIZER_PYTHON: python },
        timeout: 10_000,
        windowsHide: true,
      }),
      (error) => /must be a regular directory, not a link/.test(error.stderr),
    );
  } finally {
    await rm(link, { force: true });
  }
}

const root = await makeProject();
try {
  assert.equal(
    await readFile(join(pluginDirectory, ".gitignore"), "utf8").then((text) => text.includes("node_modules/")),
    true,
  );
  await protocolRun(root, "auto");
  await protocolRun(root, "legacy");
  await testDescribeAndFreshness(root);
  await protocolRun(root, "auto-after-rebuild");
  await testRootSymlinkRejected(root);
  await testDependencyContradiction(root);
} finally {
  await rm(root, { recursive: true, force: true });
}

console.log("PASS project-organizer MCP: 4 read-only tools, bounded SQLite queries, no write surface");
