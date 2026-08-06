import {
  copyFileSync,
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  writeFileSync,
} from "node:fs";
import { dirname, join, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

export const P6_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
export function parseArgs(argv, allowed) {
  const result = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--") || !allowed.includes(token)) {
      throw new Error(`Unknown argument: ${token}`);
    }
    const value = argv[index + 1];
    if (value === undefined || value.startsWith("--")) {
      throw new Error(`Missing value for ${token}.`);
    }
    result[token.slice(2)] = value;
    index += 1;
  }
  return result;
}

export function requireRunRoot(value) {
  if (!value || !String(value).trim()) throw new Error("--run-root is required.");
  const root = resolve(String(value));
  const filesystemRoot = resolve(root, sep);
  if (root === filesystemRoot || root === P6_ROOT) {
    throw new Error(`Refusing unsafe run root: ${root}`);
  }
  return root;
}

export function readText(path) {
  return readFileSync(path, "utf8").replace(/^\uFEFF/, "");
}

export function writeText(path, value) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, value, "utf8");
}

export function writeJson(path, value) {
  writeText(path, `${JSON.stringify(value, null, 2)}\n`);
}

export function listFiles(root) {
  if (!existsSync(root)) return [];
  const files = [];
  const walk = (directory) => {
    for (const entry of readdirSync(directory, { withFileTypes: true })) {
      const absolute = join(directory, entry.name);
      if (entry.isDirectory()) walk(absolute);
      else if (entry.isFile()) files.push(absolute);
    }
  };
  walk(root);
  return files.sort((a, b) => a.localeCompare(b));
}

export function copyFile(source, destination) {
  mkdirSync(dirname(destination), { recursive: true });
  copyFileSync(source, destination);
}

export function copyTree(source, destination) {
  for (const file of listFiles(source)) {
    copyFile(file, join(destination, relative(source, file)));
  }
}

export function isMain(metaUrl) {
  return Boolean(process.argv[1]) && resolve(process.argv[1]) === fileURLToPath(metaUrl);
}
