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
const siteHtml = fs.readFileSync(path.join(root, "site.html"), "utf8");
const content = loadContent();

// Required assets
for (const file of [
  "index.html",
  "site.html",
  "styles.css",
  "script.js",
  "content.js",
  "og-image.jpg",
  "share.jpg",
  "cv.pdf",
  "cv-en.pdf",
  "photo.png",
  "photo.webp",
  "photo.avif",
  "robots.txt",
  "vercel.json",
  "favicon.svg",
  "site.webmanifest",
]) {
  if (!fs.existsSync(path.join(root, file))) fail(`Missing file: ${file}`);
}

// robots + meta noindex
const robots = fs.readFileSync(path.join(root, "robots.txt"), "utf8");
if (!/User-agent:\s*Googlebot[\s\S]*Disallow:\s*\//.test(robots)) {
  fail("robots.txt should Disallow / for Googlebot");
}
if (!/User-agent:\s*TelegramBot[\s\S]*Allow:\s*\//.test(robots)) {
  fail("robots.txt should Allow / for TelegramBot (link previews)");
}
if (/User-agent:\s*\*[\s\S]*Disallow:\s*\/\s*$/m.test(robots)) {
  fail("robots.txt: User-agent * Disallow / blocks Telegram when UA is not TelegramBot");
}
if (html.includes('name="robots"') && html.includes("noindex")) {
  fail("index.html: global robots noindex blocks Telegram previews; use googlebot/bingbot only");
}
if (!html.includes('property="og:image"')) fail("index.html missing og:image meta");
if (html.includes("heroName")) fail("index.html must be OG-only (full site is site.html)");
if (!siteHtml.includes('id="heroName"')) fail("site.html missing hero markup");
if (!siteHtml.includes('rel="canonical"') || !siteHtml.includes("/site")) {
  fail("site.html canonical should point at /site");
}
if (!html.includes("/?v=2")) fail("index.html OG landing should reference /?v=2");
if (!content.meta?.siteUrl?.startsWith("https://")) fail("content.meta.siteUrl must be absolute https URL");
if (!content.meta?.email?.includes("@")) fail("content.meta.email is required");
if (!siteHtml.includes("mailto:" + content.meta.email)) fail("site.html missing mailto for meta.email");
if (!siteHtml.includes('id="cvDownload"')) fail("site.html missing #cvDownload");
if (!content.meta?.pdf?.uk?.href || !content.meta?.pdf?.en?.href) {
  fail("content.meta.pdf must define uk and en downloads");
}
if (!siteHtml.includes("photo.webp")) fail("site.html should use photo.webp");
if (!siteHtml.includes('id="competencies"')) fail("legacy #competencies anchor alias missing");

const vercel = JSON.parse(fs.readFileSync(path.join(root, "vercel.json"), "utf8"));
const xRobots = vercel.headers?.some((h) =>
  h.headers?.some((x) => x.key === "X-Robots-Tag" && x.value.includes("noindex"))
);
if (xRobots) fail("vercel.json X-Robots-Tag noindex blocks Telegram link previews");

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
const i18nInHtml = [...siteHtml.matchAll(/data-i18n="([^"]+)"/g)].map((m) => m[1]);
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
const sectionIds = [...siteHtml.matchAll(/<section[^>]+id="([^"]+)"/g)].map((m) => m[1]);
const navHrefs = [...siteHtml.matchAll(/href="#([^"]+)" class="nav__link/g)].map((m) => m[1]);
for (const href of navHrefs) {
  if (!sectionIds.includes(href)) fail(`Nav href #${href} has no matching section id`);
}
if (navHrefs.includes("competencies")) fail("nav should not list removed competencies section");

// DOM ids used in script.js
const script = fs.readFileSync(path.join(root, "script.js"), "utf8");
if (!script.includes("atEnd") || !script.includes("langFromUrl")) {
  fail("script.js should handle end-of-page nav and ?lang=");
}
const idsInScript = [...script.matchAll(/getElementById\("([^"]+)"\)/g)].map((m) => m[1]);
for (const id of idsInScript) {
  if (!siteHtml.includes(`id="${id}"`)) fail(`script.js expects #${id} but site.html has no such id`);
}

// Data arrays
for (const name of ["industries", "impact", "roles", "experience", "expertise", "certification"]) {
  if (!content[name]) fail(`Missing content.${name}`);
  else countArrayPairs(content, name);
}
if (content.specializations) fail("specializations should be merged into expertise");
if (content.expertise.uk.length !== 5) fail("expertise should have 5 competency cards");
if (content.impact.uk.length !== 5) fail("impact should have 5 cards");

// Early career compressed (no separate Play Mobile company row with role)
const earlyUk = content.experience.uk.find((j) => /Ранній|2005/.test(j.company + j.period));
const earlyEn = content.experience.en.find((j) => /Earlier|2005/.test(j.company + j.period));
if (!earlyUk || !earlyEn) fail("Early career entry missing");
if (earlyUk.role || earlyEn.role) fail("Early career should not have a role field");

const lokoUk = content.experience.uk.find((j) => j.company.includes("LOKO"));
if (!lokoUk?.role?.includes("Заступник") || /CBDM/i.test(lokoUk.role)) {
  fail("LOKO role must keep Заступник title without mismatched CBDM label");
}
const bannedPhrases = [
  "не свідчення",
  "не побудований",
  "не розробник",
  "не одноосібний",
  "не були основною зоною",
  "not the primary mandate",
  "not a built facility",
  "not a developer",
  "Overall LOKO P&L",
  "Загальний P&L LOKO",
  "кандидат готував",
  "деталі під NDA",
  "details under NDA",
];
const blob = JSON.stringify(content.experience);
for (const phrase of bannedPhrases) {
  if (blob.includes(phrase)) fail(`Internal accuracy note leaked into CV: ${phrase}`);
}
const alloGroup = content.experience.uk.find((j) => j.roles?.length);
if (!alloGroup) fail("ALLO career must be grouped as one employer with roles[]");
const alloSales = alloGroup.roles.find((r) => /2012/.test(r.period));
if (!alloSales?.intro?.includes("150+")) fail("150+ headcount must sit on ALLO sales 2012–2016");
if (!alloGroup.project || !/Oracle|JD Edwards/i.test(alloGroup.project.role)) {
  fail("Oracle JD Edwards must be a project within the ALLO employer group");
}

// Meta
if (!content.meta.phone.startsWith("+")) warn("meta.phone should be E.164");
if (!content.meta.linkedin.includes("linkedin.com")) fail("Invalid LinkedIn URL");
if (content.meta.email !== "parshencevdenis@gmail.com") fail("Unexpected email");
if (!content.meta.phoneDisplay.uk.includes("+380 50")) fail("UA phone display should use +380 format");
if (content.meta.pdf.uk.href !== "cv.pdf" || content.meta.pdf.en.href !== "cv-en.pdf") {
  fail("PDF hrefs must be language-specific");
}
if (!content.roles.uk[0].includes("Операційний директор")) fail("First target role should be COO");
if (!content.roles.uk.some((r) => /CEO невеликого/i.test(r))) fail("CEO of small business role missing");
if (content.roles.uk.some((r) => /CEO.*COO|COO.*CEO/.test(r))) {
  fail("CEO and COO must not be combined in one role string");
}
if (!/64 міст/i.test(content.impact.uk[0].desc)) fail("First impact card should cover 64 cities expansion");
if (!/150\+/.test(content.impact.uk[1].metric + content.impact.uk[1].desc)) {
  fail("Second impact card must cover 150+ ALLO operating structure");
}
if (!/4–5|4-5/.test(content.impact.uk[2].metric)) fail("Third impact card must cover 4–5 function leads");
if (!/оборот/i.test(content.impact.uk[3].desc) || !/квітн/i.test(content.impact.uk[3].desc)) {
  fail("×16 impact must state turnover + period");
}
if (!content.impact.uk[3].note) fail("×16 card needs business-outcome note");
if (!/Oracle|JD Edwards/i.test(content.impact.uk[4].desc + content.impact.uk[4].metric)) {
  fail("Fifth impact card should cover Oracle JD Edwards ERP");
}
if (/по теперішній|Поточний час/.test(JSON.stringify(content.experience.uk))) {
  fail("Experience periods should use «дотепер», not «по теперішній / Поточний»");
}
if (/проект[^і]|проектуван|рітейлер/.test(JSON.stringify(content.experience.uk) + JSON.stringify(content.expertise.uk))) {
  fail("Ukrainian copy should use проєкт / проєктування / ритейлер spelling");
}
if (!/Незавершена вища/.test(content.certification.uk[0].text)) {
  fail("Education must state incomplete higher education");
}
if (!siteHtml.includes("mailto:parshencevdenis@gmail.com")) fail("site contact mailto missing");
if (!/html\.js-anim \.reveal/.test(fs.readFileSync(path.join(root, "styles.css"), "utf8"))) {
  fail("styles.css should gate reveal animation behind html.js-anim");
}
if (!script.includes("writeStoredLang") || !script.includes("readStoredLang")) {
  fail("script.js should guard localStorage access");
}
if (!/header\.offsetHeight \+ 84/.test(script)) {
  fail("updatePageNav offset should align with scroll-margin (~header+84)");
}

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
console.log("✓ SEO block (robots.txt, search-bot noindex) OK");
console.log("\nAll checks passed.\n");
