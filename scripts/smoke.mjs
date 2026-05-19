/**
 * Smoke test production deployment.
 * Run: node scripts/smoke.mjs [baseUrl]
 */
const base = (process.argv[2] || "https://parshentsev-cv.vercel.app").replace(/\/$/, "");
const paths = [
  "/",
  "/?v=2",
  "/robots.txt",
  "/favicon.svg",
  "/site.webmanifest",
  "/cv.pdf",
  "/og-image.jpg",
  "/share.jpg",
  "/photo.png",
  "/styles.css",
  "/script.js",
  "/content.js",
  "/site",
];
const errors = [];

// Root should redirect to /?v=2 (Telegram preview URL)
{
  const res = await fetch(`${base}/`, { redirect: "manual" });
  const loc = res.headers.get("location") || "";
  if (res.status < 300 || res.status >= 400 || !loc.includes("v=2")) {
    errors.push(`/: should redirect to /?v=2 (got ${res.status} ${loc})`);
  }
}

for (const p of paths) {
  const url = `${base}${p}`;
  const res = await fetch(url, { redirect: "follow" });
  if (!res.ok) errors.push(`${p}: HTTP ${res.status}`);
  else if (p === "/?v=2") {
    const html = await res.text();
    if (!html.includes('property="og:image"')) errors.push("/?v=2: missing og:image");
    if (!html.includes("?v=2")) errors.push("/?v=2: og:url should reference ?v=2");
    if (html.includes("heroName")) errors.push("/?v=2: should be OG-only landing");
  } else if (p === "/") {
    const html = await res.text();
    if (html.includes("heroName")) errors.push("/: should be OG-only landing (use /site for full CV)");
    if (html.includes('name="robots"') && html.includes("noindex")) {
      errors.push("/: global robots noindex should not be set (Telegram previews)");
    }
    if (!html.includes('property="og:image"')) errors.push("/: missing og:image meta");
    if (html.length > 4000) errors.push("/: page too large for Telegram crawler");
  }
  if (p === "/site") {
    const html = await res.text();
    if (!html.includes("heroName")) errors.push("/site: missing hero markup");
  }
  if (p === "/robots.txt") {
    const text = await res.text();
    if (!text.includes("Disallow: /")) errors.push("robots.txt: missing Disallow");
  }
  const xRobots = res.headers.get("x-robots-tag");
  if (xRobots && xRobots.includes("noindex")) {
    errors.push(`${p}: X-Robots-Tag noindex blocks Telegram (${xRobots})`);
  }
}

if (errors.length) {
  console.error("Smoke test failed for", base);
  errors.forEach((e) => console.error("  ✗", e));
  process.exit(1);
}
console.log("✓ Smoke test passed for", base);
for (const p of paths) console.log("  ", p);
