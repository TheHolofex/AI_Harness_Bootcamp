#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { FIGURE_TEMPLATES } from "./resource-figure-kit.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SITE = path.join(ROOT, "site");
const CATALOG = JSON.parse(fs.readFileSync(path.join(ROOT, "resources", "catalog.json"), "utf8"));
const SCOPES = JSON.parse(fs.readFileSync(path.join(ROOT, "resources", "scopes.json"), "utf8"));
const errors = [];
const warnings = [];

function fail(message) { errors.push(message); }
function warn(message) { warnings.push(message); }
function rel(file) { return path.relative(ROOT, file).replaceAll(path.sep, "/"); }
function text(file) { return fs.readFileSync(file, "utf8"); }
function walk(dir, predicate = () => true) {
  if (!fs.existsSync(dir)) return [];
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const target = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...walk(target, predicate));
    else if (predicate(target)) files.push(target);
  }
  return files;
}

function stripMarkup(value) {
  return value
    .replace(/<script\b[\s\S]*?<\/script>/gi, " ")
    .replace(/<style\b[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&(?:nbsp|amp|lt|gt|quot|#39);/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function wordCount(value) {
  return stripMarkup(value).split(/\s+/).filter(Boolean).length;
}

function exactPathExists(target) {
  const absolute = path.resolve(target);
  const relative = path.relative(ROOT, absolute);
  if (relative.startsWith("..") || path.isAbsolute(relative)) return fs.existsSync(absolute);
  let cursor = ROOT;
  for (const part of relative.split(path.sep).filter(Boolean)) {
    if (!fs.existsSync(cursor) || !fs.statSync(cursor).isDirectory()) return false;
    if (!fs.readdirSync(cursor).includes(part)) return false;
    cursor = path.join(cursor, part);
  }
  return fs.existsSync(cursor);
}

function idsIn(value) {
  const ids = [];
  for (const match of value.matchAll(/\bid\s*=\s*["']([^"']+)["']/gi)) ids.push(match[1]);
  return ids;
}

function validatePortfolioContracts() {
  const expected = ["PW-2", "PW-4", "P1-2", "P1-5", "P2-1", "P2-2", "P3-1", "P3-3", "P4-1", "P4-5", "P5-3", "P6-2", "P6-5", "P7-1", "P7-4", "P8-2", "P8-5", "PC-1"];
  const actual = CATALOG.resources.map((item) => item.id);
  if (JSON.stringify(actual) !== JSON.stringify(expected)) fail("catalog Wave 1 IDs/order do not match the approved slate");
  for (const resource of CATALOG.resources) {
    if (resource.status !== "published") fail(`${resource.id}: approved Wave 1 resource is not published`);
  }
  if (SCOPES.neverRender !== true) fail("scopes.json must declare neverRender=true");
  const scopeIds = SCOPES.resources.map((item) => item.id);
  for (const id of expected) {
    if (!scopeIds.includes(id)) fail(`${id}: missing internal scope contract`);
    const resource = CATALOG.resources.find((item) => item.id === id);
    const scope = SCOPES.resources.find((item) => item.id === id);
    if (!resource || !scope) continue;
    if (!scope.startsWherePageEnds || !scope.pageOwns || !scope.doNotRetell?.length) fail(`${id}: incomplete anti-duplication contract`);
    const canonical = path.join(ROOT, resource.canonical.path);
    if (!exactPathExists(canonical)) fail(`${id}: canonical file is absent or case-mismatched: ${resource.canonical.path}`);
    if (resource.canonical.fragment) {
      const target = text(canonical);
      if (!new RegExp(`\\bid=["']${resource.canonical.fragment.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}["']`).test(target)) {
        fail(`${id}: canonical fragment is absent: ${resource.canonical.path}#${resource.canonical.fragment}`);
      }
    }
  }
  const rendered = walk(SITE, (file) => /\.(?:html|svg|js|json)$/i.test(file)).map(text).join("\n");
  const scopeNeedles = ["startsWherePageEnds", "doNotRetell", "portfolioCollisionRules", "canonicalOwner"];
  for (const needle of scopeNeedles) if (rendered.includes(needle)) fail(`internal scope field leaked into site output: ${needle}`);
}

const makingOf = [
  /this handout covers/i,
  /in this resource[, ]/i,
  /the learning objective/i,
  /canonical owner/i,
  /scope rail/i,
  /collision id/i,
  /production wave/i,
  /\bwave\s+[1-9]\b/i,
  /reviewer (?:said|found|requested)/i,
  /generated page/i,
  /design rationale/i
];
const staffLeak = [
  /FACILITATOR_KEY/i,
  /ANSWER_KEY/i,
  /COHORT_PIN/i,
  /prework\/FACILITATOR_NOTES/i,
  /lead\/MANY_MINDS_ANSWER_KEY/i,
  /intake_poisoned/i,
  /P_(?:contradiction|false_citation|hostile)\.md/i
];
const driftPatterns = [
  /\b(?:gpt|claude|grok)-\d[\w.-]*/i,
  /\b(?:winget|choco|scoop|npm|pip)\s+install\b/i,
  /\bversion\s+\d+\.\d+(?:\.\d+)?\b/i
];
const ritualPatterns = [
  /break it on purpose/i,
  /deliberately\s+(?:break|delete|remove|fail)/i,
  /inject\s+(?:a|the)\s+failure/i,
  /\bpredict(?:ion)?\b[^.]{0,120}\breveal\b/i,
  /\breveal\b[^.]{0,120}\bpredict(?:ion)?\b/i,
  /forced disagreement/i,
  /adversarial review/i,
  /cannot make[^.]{0,100}fail/i
];

function scanLearnerText(label, value, resourceId = "") {
  for (const pattern of makingOf) if (pattern.test(value)) fail(`${label}: making-of language matched ${pattern}`);
  for (const pattern of staffLeak) if (pattern.test(value)) fail(`${label}: staff/answer material matched ${pattern}`);
  for (const pattern of driftPatterns) if (pattern.test(stripMarkup(value))) fail(`${label}: tool/version drift pattern matched ${pattern}`);
  for (const pattern of ritualPatterns) if (pattern.test(stripMarkup(value))) fail(`${label}: forced-failure or reveal ritual matched ${pattern}`);
  if (resourceId === "P5-3") {
    const p5Patterns = [
      /\b(?:which|these|the)\s+intake\s+(?:items?|files?)\s+(?:is|are|were)\s+(?:poisoned|hostile|false)/i,
      /\b(?:three|3)\s+(?:poisoned|hostile|bad)\s+(?:items?|files?)/i,
      /mission_flesh\/p5\/intake/i
    ];
    for (const pattern of p5Patterns) if (pattern.test(value)) fail(`${label}: P5 spoiler-risk pattern matched ${pattern}`);
  }
}

function validateSourcesAndFigures() {
  const paragraphOwners = new Map();
  const sourceDocs = [];
  for (const resource of CATALOG.resources) {
    const source = path.join(ROOT, "resources", "handouts", resource.module, `${resource.slug}.html`);
    const figures = path.join(ROOT, "resources", "figures", resource.module, `${resource.id}.json`);
    if (!fs.existsSync(source) && resource.status === "published") fail(`${resource.id}: published source missing`);
    if (!fs.existsSync(figures) && resource.status === "published") fail(`${resource.id}: published figure spec missing`);
    if (!fs.existsSync(source) && !fs.existsSync(figures)) continue;
    if (!fs.existsSync(source) || !fs.existsSync(figures)) {
      fail(`${resource.id}: source and figure spec must land together`);
      continue;
    }
    const body = text(source);
    const specRaw = text(figures);
    let spec;
    try { spec = JSON.parse(specRaw); } catch (error) { fail(`${resource.id}: invalid figure JSON: ${error.message}`); continue; }
    scanLearnerText(rel(source), body, resource.id);
    scanLearnerText(rel(figures), specRaw, resource.id);
    if (/<h1\b/i.test(body)) fail(`${resource.id}: source fragment must not contain h1`);
    for (const requiredId of ["purpose", "mechanism", "worked-case", "practice", "transfer"]) {
      if (resource.id !== "PC-1" && !new RegExp(`<section\\b[^>]*\\bid=["']${requiredId}["']`, "i").test(body)) fail(`${resource.id}: missing learning-arc section #${requiredId}`);
    }
    if (resource.id !== "PC-1") {
      const words = wordCount(body);
      // A linked field guide may be a short troubleshooting route or a deeper
      // technical reference. Production completeness is enforced by the
      // required mechanism, worked-case, practice, transfer, and Sources
      // sections—not by padding every guide to a classroom-sized word count.
      if (words < 700 || words > 4000) fail(`${resource.id}: ${words} words; expected 700–4,000`);
      if (!/>Sources\b/i.test(body)) fail(`${resource.id}: missing Sources shelf`);
      if (!/<table\b/i.test(body)) warn(`${resource.id}: no table found; confirm the evidence artifact is still inspectable`);
    } else {
      const words = wordCount(body);
      if (words > 1500) fail(`PC-1: ${words} words cannot plausibly fit a one-page retrieval card`);
    }
    if (spec.schemaVersion !== 1 || spec.resourceId !== resource.id || !Array.isArray(spec.figures)) fail(`${resource.id}: figure spec header is invalid`);
    const requiredRoles = resource.figurePolicy === "normal" ? ["orientation", "mechanism", "diagnostic"] : ["compact"];
    if (spec.figures?.length !== requiredRoles.length) fail(`${resource.id}: figure policy requires exactly ${requiredRoles.length} figure(s)`);
    const seenIds = new Set();
    for (const figure of spec.figures || []) {
      if (seenIds.has(figure.id)) fail(`${resource.id}: duplicate figure id ${figure.id}`);
      seenIds.add(figure.id);
      for (const key of ["id", "role", "template", "title", "desc", "caption", "transcript"]) if (!figure[key]) fail(`${resource.id}/${figure.id || "figure"}: missing ${key}`);
      if (!requiredRoles.includes(figure.role)) fail(`${resource.id}: unexpected figure role ${figure.role}`);
      if (!FIGURE_TEMPLATES.includes(figure.template)) fail(`${resource.id}: unsupported figure template ${figure.template}`);
      if ((figure.desc || "").length < 45) fail(`${resource.id}/${figure.id}: description is too thin`);
      if ((figure.transcript || "").length < 120) fail(`${resource.id}/${figure.id}: transcript is too thin`);
      const marker = new RegExp(`<figure\\s+data-resource-figure=["']${figure.role}["']\\s*><\\/figure>`, "i");
      if (!marker.test(body)) fail(`${resource.id}: body missing marker for figure role ${figure.role}`);
    }
    const markerCount = (body.match(/data-resource-figure=/g) || []).length;
    if (markerCount !== requiredRoles.length) fail(`${resource.id}: source has ${markerCount} figure markers; expected ${requiredRoles.length}`);
    for (const match of body.matchAll(/<p\b[^>]*>([\s\S]*?)<\/p>/gi)) {
      const normalized = stripMarkup(match[1]).toLowerCase().replace(/[^a-z0-9 ]/g, "").replace(/\s+/g, " ").trim();
      if (normalized.length < 120) continue;
      if (paragraphOwners.has(normalized)) fail(`${resource.id}: duplicate substantive paragraph also appears in ${paragraphOwners.get(normalized)}`);
      else paragraphOwners.set(normalized, resource.id);
    }
    sourceDocs.push({ id: resource.id, value: stripMarkup(body).toLowerCase() });
  }
  for (let i = 0; i < sourceDocs.length; i++) {
    for (let j = i + 1; j < sourceDocs.length; j++) {
      const score = jaccard(shingles(sourceDocs[i].value, 5), shingles(sourceDocs[j].value, 5));
      if (score > 0.82) fail(`${sourceDocs[i].id}/${sourceDocs[j].id}: five-word-shingle similarity ${score.toFixed(2)}`);
      else if (score > 0.55) warn(`${sourceDocs[i].id}/${sourceDocs[j].id}: editorial similarity review ${score.toFixed(2)}`);
    }
  }
}

function shingles(value, size) {
  const words = value.replace(/[^a-z0-9 ]/g, " ").split(/\s+/).filter(Boolean);
  const set = new Set();
  for (let i = 0; i <= words.length - size; i++) set.add(words.slice(i, i + size).join(" "));
  return set;
}

function jaccard(a, b) {
  if (!a.size && !b.size) return 1;
  let intersection = 0;
  for (const value of a) if (b.has(value)) intersection++;
  return intersection / (a.size + b.size - intersection);
}

function validateSvg(file) {
  const value = text(file);
  const result = spawnSync("/usr/bin/xmllint", ["--noout", file], { encoding: "utf8" });
  if (result.error) fail(`${rel(file)}: xmllint is unavailable: ${result.error.message}`);
  else if (result.status !== 0) fail(`${rel(file)}: xmllint failed: ${(result.stderr || result.stdout || "unknown XML error").trim()}`);
  if (!/<svg\b[^>]*xmlns="http:\/\/www\.w3\.org\/2000\/svg"/i.test(value)) fail(`${rel(file)}: missing SVG namespace`);
  if (!/viewBox="0 0 1120 280"/.test(value)) fail(`${rel(file)}: viewBox must be 0 0 1120 280`);
  if (!/role="img"/.test(value) || !/aria-labelledby=/.test(value) || !/<title\b/.test(value) || !/<desc\b/.test(value)) fail(`${rel(file)}: accessible SVG title/description contract failed`);
  if (/<(?:script|foreignObject)\b/i.test(value) || /(?:href|src)="https?:/i.test(value)) fail(`${rel(file)}: active or external SVG content is forbidden`);
  const ids = idsIn(value);
  if (new Set(ids).size !== ids.length) fail(`${rel(file)}: duplicate SVG ids`);
  for (const match of value.matchAll(/url\(#([^)]+)\)/g)) if (!ids.includes(match[1])) fail(`${rel(file)}: unresolved SVG reference #${match[1]}`);
  for (const match of value.matchAll(/font-size:\s*(\d+(?:\.\d+)?)px/g)) if (Number(match[1]) < 14) fail(`${rel(file)}: figure text below 14px`);
  for (const match of value.matchAll(/<(?:rect|circle|text)\b([^>]*)>/g)) {
    const attrs = Object.fromEntries([...match[1].matchAll(/\b(x|y|cx|cy|width|height)="(-?\d+(?:\.\d+)?)"/g)].map((item) => [item[1], Number(item[2])]));
    if ((attrs.x ?? attrs.cx ?? 0) < 0 || (attrs.y ?? attrs.cy ?? 0) < 0) fail(`${rel(file)}: negative element coordinate`);
    if ((attrs.x ?? attrs.cx ?? 0) > 1120 || (attrs.y ?? attrs.cy ?? 0) > 280) fail(`${rel(file)}: element origin outside viewBox`);
    if (attrs.width !== undefined && attrs.width <= 0) fail(`${rel(file)}: non-positive width`);
    if (attrs.height !== undefined && attrs.height <= 0) fail(`${rel(file)}: non-positive height`);
    if (attrs.x !== undefined && attrs.width !== undefined && attrs.x + attrs.width > 1120.01) fail(`${rel(file)}: rectangle exceeds viewBox width`);
    if (attrs.y !== undefined && attrs.height !== undefined && attrs.y + attrs.height > 280.01) fail(`${rel(file)}: rectangle exceeds viewBox height`);
  }
}

function validateOwnerReturn(label, value, ownerHref) {
  const ownerLinks = value.split(`href="${ownerHref}"`).length - 1;
  if (ownerLinks < 3) fail(`${label}: owning course route is not prominent in the page header and footer`);
  const plate = value.match(/<nav class="resource-plate"[^>]*>[\s\S]*?<\/nav>/i)?.[0];
  if (!plate) {
    fail(`${label}: missing return-to-course navigation`);
    return;
  }
  const plateHrefs = [...plate.matchAll(/\bhref=["']([^"']+)["']/gi)].map((match) => match[1]);
  if (plateHrefs.length !== 1 || plateHrefs[0] !== ownerHref) {
    fail(`${label}: bottom navigation must return only to its owning course route`);
  }
}

function validateGenerated() {
  const published = CATALOG.resources.filter((item) => item.status === "published");
  const expectedHtml = new Set();
  const expectedSvg = new Set();
  for (const resource of published) {
    expectedHtml.add(path.join(SITE, "resources", resource.module, `${resource.slug}.html`));
    const spec = JSON.parse(text(path.join(ROOT, "resources", "figures", resource.module, `${resource.id}.json`)));
    for (const figure of spec.figures) expectedSvg.add(path.join(SITE, "assets", "resources", resource.module, `${figure.id}.svg`));
  }
  for (const file of expectedHtml) if (!fs.existsSync(file)) fail(`missing generated page ${rel(file)}`);
  for (const file of expectedSvg) if (!fs.existsSync(file)) fail(`missing generated figure ${rel(file)}`);
  for (const file of walk(path.join(SITE, "resources"), (item) => item.endsWith(".html"))) if (!expectedHtml.has(file)) fail(`orphan generated page ${rel(file)}`);
  for (const file of walk(path.join(SITE, "assets", "resources"), (item) => item.endsWith(".svg"))) if (!expectedSvg.has(file)) fail(`orphan generated figure ${rel(file)}`);
  for (const file of expectedHtml) {
    if (!fs.existsSync(file)) continue;
    const value = text(file);
    scanLearnerText(rel(file), value, path.basename(file, ".html"));
    if (!value.startsWith("<!-- GENERATED by scripts/build-resources.mjs. DO NOT EDIT. -->")) fail(`${rel(file)}: generated ownership marker missing`);
    const h1 = (value.match(/<h1\b/gi) || []).length;
    if (h1 !== 1) fail(`${rel(file)}: expected one h1, found ${h1}`);
    const ids = idsIn(value);
    if (new Set(ids).size !== ids.length) fail(`${rel(file)}: duplicate HTML ids`);
    for (const match of value.matchAll(/<img\b([^>]*)>/gi)) if (!/\balt="[^"]*"/.test(match[1])) fail(`${rel(file)}: image without alt`);
    if (/\/(?:Users|home)\//.test(value) || /file:\/\//i.test(value) || /localhost(?::\d+)?/i.test(value)) fail(`${rel(file)}: local workstation reference leaked`);
    const generatedPath = rel(file);
    const resource = published.find((item) => generatedPath === `site/resources/${item.module}/${item.slug}.html`);
    if (resource) {
      const fragment = resource.canonical.fragment ? `#${resource.canonical.fragment}` : "";
      const ownerHref = `../../${resource.canonical.path.replace(/^site\//, "")}${fragment}`;
      validateOwnerReturn(generatedPath, value, ownerHref);
    }
    const tidy = spawnSync("/usr/bin/tidy", ["-qe", "--new-blocklevel-tags", "header,nav,main,section,article,footer,figure,figcaption,details,summary", file], { encoding: "utf8" });
    if (tidy.error) warn(`${rel(file)}: tidy unavailable; HTML structural checks still ran`);
    else if (tidy.status !== null && tidy.status >= 2) fail(`${rel(file)}: tidy found HTML errors: ${(tidy.stderr || tidy.stdout || "unknown HTML error").trim().split("\n").slice(0, 3).join(" | ")}`);
  }
  for (const file of expectedSvg) if (fs.existsSync(file)) validateSvg(file);
  const builtCorpus = [...expectedHtml, ...expectedSvg].filter(fs.existsSync).map(text).join("\n");
  if (/startsWherePageEnds|doNotRetell|canonicalOwner|portfolioCollisionRules/.test(builtCorpus)) fail("internal scope metadata appears in generated resource output");
  if (fs.existsSync(path.join(SITE, "resources.html"))) fail("obsolete generated page site/resources.html");
}

function validateLinks() {
  const htmlFiles = walk(SITE, (file) => file.endsWith(".html"));
  for (const file of htmlFiles) {
    const value = text(file);
    for (const match of value.matchAll(/\b(href|src)=["']([^"']+)["']/gi)) {
      const attribute = match[1].toLowerCase();
      const raw = match[2];
      const visiblePath = raw.split(/[?#]/, 1)[0];
      if (attribute === "href" && /\.(?:md|markdown)$/i.test(visiblePath)) {
        fail(`${rel(file)}: visible link exposes raw Markdown ${raw}`);
        continue;
      }
      if (/^(?:https?:|mailto:|tel:|data:|javascript:)/i.test(raw) || raw === "#") continue;
      const [rawPath, fragment = ""] = raw.split("#", 2);
      let target;
      if (!rawPath) target = file;
      else if (rawPath.startsWith("/site/")) target = path.join(ROOT, rawPath.slice(1));
      else if (rawPath.startsWith("/")) { warn(`${rel(file)}: root-absolute local link ${raw}`); continue; }
      else target = path.resolve(path.dirname(file), decodeURIComponent(rawPath.split("?")[0]));
      if (!exactPathExists(target)) { fail(`${rel(file)}: missing or case-mismatched local target ${raw}`); continue; }
      if (fragment && target.endsWith(".html")) {
        const targetText = text(target);
        const escaped = fragment.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
        if (!new RegExp(`\\b(?:id|name)=["']${escaped}["']`).test(targetText)) fail(`${rel(file)}: missing fragment ${raw}`);
      }
      if (staffLeak.some((pattern) => pattern.test(raw))) fail(`${rel(file)}: link names staff-only material: ${raw}`);
    }
  }
  for (const resource of CATALOG.resources.filter((item) => item.status === "published")) {
    const module = CATALOG.modules.find((item) => item.id === resource.module);
    const owner = path.join(ROOT, module?.canonicalPath || resource.canonical.path);
    const expected = `resources/${resource.module}/${resource.slug}.html`;
    if (!text(owner).includes(expected)) fail(`${resource.id}: owning learner page lacks contextual inbound link containing ${expected}`);
  }
}

function main() {
  validatePortfolioContracts();
  validateSourcesAndFigures();
  validateGenerated();
  validateLinks();
  for (const message of warnings) process.stdout.write(`WARN ${message}\n`);
  process.stdout.write(`Manual gates: source entailment, rendered figure legibility/meaning, cross-module semantic deduplication, desktop/mobile inspection, and exact one-page PC-1 print.\n`);
  if (errors.length) {
    for (const message of errors) process.stderr.write(`ERROR ${message}\n`);
    process.stderr.write(`Resource verification failed with ${errors.length} error(s) and ${warnings.length} warning(s).\n`);
    process.exitCode = 1;
    return;
  }
  process.stdout.write(`Resource verification passed with ${warnings.length} warning(s).\n`);
}

main();
