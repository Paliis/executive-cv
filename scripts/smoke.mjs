/**
 * Smoke test production deployment.
 * Run: node scripts/smoke.mjs [baseUrl]
 */
const base = (process.argv[2] || "https://parshentsev-cv.vercel.app").replace(/\/$/, "");
const paths = ["/", "/robots.txt", "/cv.pdf", "/photo.png", "/styles.css", "/script.js", "/content.js"];
const errors = [];

for (const p of paths) {
  const url = `${base}${p}`;
  const res = await fetch(url, { redirect: "follow" });
  if (!res.ok) errors.push(`${p}: HTTP ${res.status}`);
  else if (p === "/") {
    const html = await res.text();
    if (!html.includes("heroName")) errors.push("/: missing hero markup");
    if (!html.includes("noindex")) errors.push("/: missing noindex meta");
  }
  if (p === "/robots.txt") {
    const text = await res.text();
    if (!text.includes("Disallow: /")) errors.push("robots.txt: missing Disallow");
  }
  const xRobots = res.headers.get("x-robots-tag");
  if (p === "/" && xRobots && !xRobots.includes("noindex")) {
    errors.push(`/: X-Robots-Tag should include noindex, got "${xRobots}"`);
  }
}

if (errors.length) {
  console.error("Smoke test failed for", base);
  errors.forEach((e) => console.error("  ✗", e));
  process.exit(1);
}
console.log("✓ Smoke test passed for", base);
for (const p of paths) console.log("  ", p);
