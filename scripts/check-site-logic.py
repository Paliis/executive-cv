"""Headless checks for CV site language, PDF link, nav, reveal, editorial."""
from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SITE = (ROOT / "site.html").as_uri()


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1366, "height": 900})

        page.goto(f"{SITE}?lang=en", wait_until="networkidle")
        page.wait_for_timeout(400)
        assert page.locator("#cvDownload").get_attribute("href") == "cv-en.pdf"
        assert page.locator("#contactEmail").inner_text() == "parshencevdenis@gmail.com"
        assert "+380" in page.locator("#contactPhone").inner_text()
        assert "COO" in page.locator(".hero__role").inner_text()
        assert page.locator(".hero__role-line").count() == 2
        assert page.locator(".lang-switch__btn.is-active").inner_text() == "EN"

        page.click("[data-lang=uk]")
        page.wait_for_timeout(300)
        assert page.locator("#cvDownload").get_attribute("href") == "cv.pdf"
        assert "lang=uk" in page.url
        assert "Операційний директор (COO)" in page.locator(".hero__role-line").first.inner_text()
        assert "Head of E" in page.locator(".hero__role-line").nth(1).inner_text()

        roles = page.locator("#rolesPills .pill").all_inner_texts()
        assert roles[0].startswith("Операційний"), roles
        assert any("CEO невеликого" in r for r in roles), roles
        assert not any("CEO" in r and "COO" in r for r in roles), roles

        impacts = page.locator(".impact-card__desc").all_inner_texts()
        assert any("оборот" in t.lower() for t in impacts), impacts
        assert any("64" in t for t in impacts), impacts
        assert page.locator(".impact-card__note").count() >= 1
        assert any("90%" in t for t in page.locator(".exp-card").filter(has_text="LOKO").all_inner_texts()), "90% should live in LOKO results"

        assert page.locator("#expertiseGrid .expertise-card").count() == 5
        assert page.locator('a.nav__link[href="#competencies"]').count() == 0

        loko = page.locator(".exp-card").filter(has_text="LOKO").first
        assert "Заступник" in loko.inner_text()
        assert "CBDM" not in loko.inner_text()

        allo = page.locator(".exp-card").filter(has_text="АЛЛО").first
        assert "2012" in allo.inner_text()
        assert "Oracle" in allo.inner_text()
        assert page.locator(".exp-card__role-block").count() >= 3
        assert page.locator("#heroCvDownload").count() == 1
        assert "Завантажити" in page.locator("#heroCvDownload").inner_text()

        opacity = page.locator(".hero__name").evaluate("el => getComputedStyle(el).opacity")
        assert float(opacity) > 0.9, opacity

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(250)
        active = page.locator(".nav__link.is-active").get_attribute("href")
        assert active == "#contact", active

        # legacy hash
        page.goto(f"{SITE}?lang=uk#competencies", wait_until="networkidle")
        page.wait_for_timeout(500)
        assert "#expertise" in page.url or page.evaluate("() => location.hash") in ("#expertise", "#competencies")

        # contact grid 2 columns on desktop
        cols = page.evaluate(
            """() => {
              const g = getComputedStyle(document.querySelector('.contact-links')).gridTemplateColumns;
              return g.split(' ').length;
            }"""
        )
        assert cols == 2, cols

        for width in (360, 390, 768):
            page.set_viewport_size({"width": width, "height": 800})
            page.wait_for_timeout(100)
            overflow = page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1")
            assert overflow is False, f"horizontal overflow at {width}"

        browser.close()

    print("Playwright checks: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
