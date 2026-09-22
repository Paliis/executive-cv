"""Headless checks for CV site language, PDF link, nav, reveal."""
from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SITE = (ROOT / "site.html").as_uri()


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page()

        page.goto(f"{SITE}?lang=en", wait_until="networkidle")
        page.wait_for_timeout(400)
        assert page.locator("#cvDownload").get_attribute("href") == "cv-en.pdf"
        assert page.locator("#contactEmail").inner_text() == "parshencevdenis@gmail.com"
        assert "+380" in page.locator("#contactPhone").inner_text()
        assert page.locator(".lang-switch__btn.is-active").inner_text() == "EN"

        page.click("[data-lang=uk]")
        page.wait_for_timeout(300)
        assert page.locator("#cvDownload").get_attribute("href") == "cv.pdf"
        assert "lang=uk" in page.url
        assert page.locator(".lang-switch__btn.is-active").inner_text() == "UA"

        roles = page.locator("#rolesPills .pill").all_inner_texts()
        assert any("Генеральний директор" in r for r in roles), roles
        assert any("Операційний директор" in r for r in roles), roles
        assert not any("CEO" in r and "COO" in r for r in roles), roles

        impacts = page.locator(".impact-card__desc").all_inner_texts()
        assert any("Оборот" in t and "дотепер" in t for t in impacts), impacts
        assert any("працівників" in t for t in impacts), impacts

        opacity = page.locator(".hero__name").evaluate("el => getComputedStyle(el).opacity")
        assert float(opacity) > 0.9, opacity

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(250)
        active = page.locator(".nav__link.is-active").get_attribute("href")
        assert active == "#contact", active

        has_anim = page.evaluate("() => document.documentElement.classList.contains('js-anim')")
        assert has_anim is True

        browser.close()

    print("Playwright checks: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
