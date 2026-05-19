/**
 * Static checks for CV site (content, HTML, assets).
 * Run: node scripts/validate.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import vm from "node:vm";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const errors = [];
const warnings = [];

function fail(msg) {
  errors.push(msg);
}
function warn(msg) {
  warnings.push(msg);
}

function loadContent() {
  const src = fs.readFileSync(path.join(root, "content.js"), "utf8");
  const sandbox = { window: {} };
  vm.runInNewContext(src, sandbox);
  return sandbox.window.CV_CONTENT;
}

function flattenKeys(obj, prefix = "") {
  const keys = [];
  for (const [k, v] of Object.entries(obj)) {
    const p = prefix ? `${prefix}.${k}` : k;
    if (v && typeof v === "object" && !Array.isArray(v) && !(k === "nav")) {
      if ("uk" in v && "en" in v && Object.keys(v).length === 2) continue;
      keys.push(...flattenKeys(v, p));
    } else if (k === "nav") {
      for (const nk of Object.keys(v)) keys.push(`${p}.${nk}`);
    } else {
      keys.push(p);
    }
  }
  return keys;
}

function langBlockKeys(block) {
  const keys = new Set();
  function walk(o, prefix) {
    for (const [k, v] of Object.entries(o)) {
      const p = prefix ? `${prefix}.${k}` : k;
      if (v && typeof v === "object" && !Array.isArray(v)) {
        walk(v, p);
      } else {
        keys.add(p);
      }
    }
  }
  walk(block, "");
  return keys;
}

function countArrayPairs(obj, name) {
  const uk = obj[name]?.uk?.length ?? -1;
  const en = obj[name]?.en?.length ?? -1;
  if (uk !== en) fail(`${name}: uk has ${uk} items, en has ${en}`);
}

const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const content = loadContent();

// Required assets
for (const file of [
  "index.html",
  "styles.css",
  "script.js",
  "content.js",
  "photo.png",
  "cv.pdf",
  "robots.txt",
  "vercel.json",
  "favicon.svg",
  "site.webmanifest",
]) {
  if (!fs.existsSync(path.join(root, file))) fail(`Missing file: ${file}`);
}

// robots + meta noindex
const robots = fs.readFileSync(path.join(root, "robots.txt"), "utf8");
if (!/Disallow:\s*\//.test(robots)) fail("robots.txt should Disallow: /");
if (!html.includes('name="robots"') || !html.includes("noindex")) fail("index.html missing noindex meta");
if (!html.includes('property="og:image"')) fail("index.html missing og:image meta");
if (!html.includes('rel="icon"')) fail("index.html missing favicon link");
if (!content.meta?.siteUrl?.startsWith("https://")) fail("content.meta.siteUrl must be absolute https URL");

const vercel = JSON.parse(fs.readFileSync(path.join(root, "vercel.json"), "utf8"));
const xRobots = vercel.headers?.some((h) =>
  h.headers?.some((x) => x.key === "X-Robots-Tag" && x.value.includes("noindex"))
);
if (!xRobots) fail("vercel.json missing X-Robots-Tag noindex header");

// i18n parity
const ukKeys = langBlockKeys(content.uk);
const enKeys = langBlockKeys(content.en);
for (const k of ukKeys) {
  if (!enKeys.has(k)) fail(`i18n: missing en key "${k}"`);
}
for (const k of enKeys) {
  if (!ukKeys.has(k)) fail(`i18n: missing uk key "${k}"`);
}

// data-i18n in HTML
const i18nInHtml = [...html.matchAll(/data-i18n="([^"]+)"/g)].map((m) => m[1]);
for (const key of i18nInHtml) {
  const parts = key.split(".");
  let ukVal = content.uk;
  let enVal = content.en;
  for (const p of parts) {
    ukVal = ukVal?.[p];
    enVal = enVal?.[p];
  }
  if (ukVal === undefined) fail(`data-i18n="${key}" not found in content.uk`);
  if (enVal === undefined) fail(`data-i18n="${key}" not found in content.en`);
}

// Section anchors vs nav
const sectionIds = [...html.matchAll(/<section[^>]+id="([^"]+)"/g)].map((m) => m[1]);
const navHrefs = [...html.matchAll(/class="nav__link"[^>]+href="#([^"]+)"/g)].map((m) => m[1]);
for (const href of navHrefs) {
  if (!sectionIds.includes(href)) fail(`Nav href #${href} has no matching section id`);
}

// DOM ids used in script.js
const script = fs.readFileSync(path.join(root, "script.js"), "utf8");
const idsInScript = [...script.matchAll(/getElementById\("([^"]+)"\)/g)].map((m) => m[1]);
for (const id of idsInScript) {
  if (!html.includes(`id="${id}"`)) fail(`script.js expects #${id} but index.html has no such id`);
}

// Data arrays
for (const name of ["industries", "impact", "specializations", "roles", "experience", "expertise", "certification"]) {
  if (!content[name]) fail(`Missing content.${name}`);
  else countArrayPairs(content, name);
}

// Experience: Play Mobile without sales manager role
const playUk = content.experience.uk.find((j) => j.company.includes("Плей"));
const playEn = content.experience.en.find((j) => /Play Mobile/i.test(j.company));
if (!playUk || !playEn) fail("Play Mobile entry missing");
if (playUk.role || playEn.role) fail("Play Mobile should not have role field");
if (/менеджер|sales manager/i.test(JSON.stringify([playUk, playEn]))) {
  fail("Play Mobile still mentions sales manager in content");
}

// Meta
if (!content.meta.phone.startsWith("+")) warn("meta.phone should be E.164");
if (!content.meta.linkedin.includes("linkedin.com")) fail("Invalid LinkedIn URL");

console.log(`\nCV site validation (${root})\n`);
if (warnings.length) {
  console.log("Warnings:");
  warnings.forEach((w) => console.log(`  ⚠ ${w}`));
}
if (errors.length) {
  console.log("Errors:");
  errors.forEach((e) => console.log(`  ✗ ${e}`));
  process.exit(1);
}
console.log(`✓ All ${i18nInHtml.length} i18n keys OK`);
console.log(`✓ ${sectionIds.length} sections, nav anchors OK`);
console.log(`✓ ${idsInScript.length} DOM ids OK`);
console.log(`✓ Content arrays uk/en parity OK`);
console.log("✓ SEO block (robots.txt, noindex) OK");
console.log("\nAll checks passed.\n");
