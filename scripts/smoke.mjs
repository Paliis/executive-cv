/**
 * Smoke test production deployment.
 * Run: node scripts/smoke.mjs [baseUrl]
 */
const base = (process.argv[2] || "https://executive-cv.vercel.app").replace(/\/$/, "");
const paths = [
  "/",
  "/robots.txt",
  "/favicon.svg",
  "/site.webmanifest",
  "/cv.pdf",
  "/og-image.jpg",
  "/photo.png",
  "/styles.css",
  "/script.js",
  "/content.js",
];
const errors = [];

// Root must not redirect (Telegram caches the first URL it sees)
{
  const res = await fetch(`${base}/`, { redirect: "manual" });
  if (res.status >= 300 && res.status < 400) {
    errors.push(`/: redirects to ${res.headers.get("location")} (use single canonical URL)`);
  } else if (!res.ok) {
    errors.push(`/: HTTP ${res.status}`);
  }
}

for (const p of paths) {
  const url = `${base}${p}`;
  const res = await fetch(url, { redirect: "follow" });
  if (!res.ok) errors.push(`${p}: HTTP ${res.status}`);
  else if (p === "/") {
    const html = await res.text();
    if (!html.includes("heroName")) errors.push("/: missing hero markup");
    if (html.includes('name="robots"') && html.includes("noindex")) {
      errors.push("/: global robots noindex should not be set (Telegram previews)");
    }
    if (!html.includes('property="og:image"')) errors.push("/: missing og:image meta");
    if (!html.includes('rel="icon"')) errors.push("/: missing favicon");
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
