#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { FIGURE_TEMPLATES, figureOutputName, renderResourceFigure } from "./resource-figure-kit.mjs";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(SCRIPT_DIR, "..");
const BOOTCAMP = path.join(ROOT, "reformation", "AI_Harness_Bootcamp_2");
const CHECK_ONLY = process.argv.includes("--check");
const REQUIRED_FIELDS = ["id", "role", "template", "title", "desc", "caption", "transcript", "eyebrow"];
const FORBIDDEN = [
  "246 kg",
  "1,404 kg",
  "3 minutes late",
  "PO-01",
  "SOURCE_EVIDENCE",
  "what we'll cover",
  "in this section"
];
const IMAGE_RE = /!\[[^\]]*]\(((?:shared\/)?figures\/[^)]+\.svg)\)/g;

function fail(message) {
  throw new Error(message);
}

function moduleDirs() {
  if (!fs.existsSync(BOOTCAMP)) return [];
  return fs.readdirSync(BOOTCAMP, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && /^module-\d{2}-/.test(entry.name))
    .map((entry) => path.join(BOOTCAMP, entry.name))
    .sort();
}

function collectMarkdown(dir) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...collectMarkdown(full));
    else if (entry.name.endsWith(".md")) out.push(full);
  }
  return out;
}

function checkForbidden(text, label) {
  for (const token of FORBIDDEN) {
    if (text.includes(token)) fail(`${label}: forbidden token ${JSON.stringify(token)}`);
  }
}

function writeFigure(file, svg) {
  const normalized = svg.endsWith("\n") ? svg : `${svg}\n`;
  if (CHECK_ONLY) {
    if (!fs.existsSync(file)) fail(`missing generated figure: ${path.relative(ROOT, file)}`);
    return;
  }
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, normalized);
}

function processModule(moduleDir) {
  const name = path.basename(moduleDir);
  const specPath = path.join(moduleDir, "figures", "spec.json");
  if (!fs.existsSync(specPath)) fail(`${name} exists without figures/spec.json`);

  let spec;
  try {
    spec = JSON.parse(fs.readFileSync(specPath, "utf8"));
  } catch (error) {
    fail(`${path.relative(ROOT, specPath)}: ${error.message}`);
  }

  const resourceId = spec.resourceId;
  if (!resourceId) fail(`${path.relative(ROOT, specPath)}: missing resourceId`);
  checkForbidden(JSON.stringify(spec), path.relative(ROOT, specPath));

  for (const figure of spec.figures || []) {
    const label = `${resourceId}/${figure.id || "?"}`;
    for (const field of REQUIRED_FIELDS) {
      if (!figure[field]) fail(`${label}: missing ${field}`);
    }
    if (!FIGURE_TEMPLATES.includes(figure.template)) {
      fail(`${label}: unsupported template ${figure.template}`);
    }
    const svg = renderResourceFigure(figure, resourceId);
    checkForbidden(svg, `${label}.svg`);
    writeFigure(path.join(moduleDir, "shared", "figures", figureOutputName(figure)), svg);
  }

  for (const md of collectMarkdown(moduleDir)) {
    const text = fs.readFileSync(md, "utf8");
    IMAGE_RE.lastIndex = 0;
    let match;
    while ((match = IMAGE_RE.exec(text))) {
      const resolved = path.normalize(path.join(path.dirname(md), match[1]));
      if (!fs.existsSync(resolved)) {
        fail(`${path.relative(ROOT, md)}: missing image ${match[1]}`);
      }
    }
  }
}

function main() {
  for (const dir of moduleDirs()) processModule(dir);
}

try {
  main();
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
