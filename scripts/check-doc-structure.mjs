#!/usr/bin/env node
// Structure check for COT docs. Zero dependencies (Node 18+ fs/promises + glob).
// - Every ADR (docs/adr/NNNN-*.md) must contain the required ADR sections.
// - Every phase PRD (docs/prd/phase-*.md) must contain Acceptance/Test/Rollback/Operability.
// Passes trivially when no matching files exist (e.g. the bootstrap commit).

import { readdir, readFile } from "node:fs/promises";
import { join } from "node:path";

const ADR_DIR = "docs/adr";
const PRD_DIR = "docs/prd";

const ADR_REQUIRED = ["## Status", "## Context", "## Options", "## Decision", "## Consequences"];
const PRD_REQUIRED = ["## Acceptance criteria", "## Test plan", "## Rollback", "## Operability"];

async function listMd(dir, filter) {
  let entries = [];
  try {
    entries = await readdir(dir);
  } catch {
    return []; // dir absent → nothing to check
  }
  return entries.filter((f) => f.endsWith(".md") && filter(f)).map((f) => join(dir, f));
}

// Case-insensitive "contains a heading that starts with X".
function hasSection(body, heading) {
  const needle = heading.toLowerCase();
  return body
    .split("\n")
    .some((line) => line.trim().toLowerCase().startsWith(needle));
}

async function check(files, required, label) {
  const problems = [];
  for (const file of files) {
    const body = await readFile(file, "utf8");
    const missing = required.filter((h) => !hasSection(body, h));
    if (missing.length) problems.push(`  ${file}: missing ${missing.join(", ")}`);
  }
  if (problems.length) {
    console.error(`✗ ${label} structure check failed:\n${problems.join("\n")}`);
    return false;
  }
  console.log(`✓ ${label}: ${files.length} file(s) OK`);
  return true;
}

const adrs = await listMd(ADR_DIR, (f) => /^\d{4}-/.test(f));
const prds = await listMd(PRD_DIR, (f) => f.startsWith("phase-"));

const ok = (await check(adrs, ADR_REQUIRED, "ADR")) & (await check(prds, PRD_REQUIRED, "phase PRD"));

if (!ok) process.exit(1);
console.log("All doc structure checks passed.");
