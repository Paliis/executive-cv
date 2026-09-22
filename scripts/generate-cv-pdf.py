"""Generate UA + EN CV PDFs aligned with site content.js editorial."""
from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "_cv-build"
FONTS = Path(r"C:\Windows\Fonts")
OUT_UK = ROOT / "cv.pdf"
OUT_EN = ROOT / "cv-en.pdf"

FONT_FILES = {
    "arial.ttf": "arial.ttf",
    "arialbd.ttf": "arialbd.ttf",
    "ariali.ttf": "ariali.ttf",
    "arialbi.ttf": "arialbi.ttf",
}

CSS = r"""
@font-face { font-family: "CV"; src: url("arial.ttf") format("truetype"); font-weight: 400; font-style: normal; font-display: block; }
@font-face { font-family: "CV"; src: url("arialbd.ttf") format("truetype"); font-weight: 700; font-style: normal; font-display: block; }
@font-face { font-family: "CV"; src: url("ariali.ttf") format("truetype"); font-weight: 400; font-style: italic; font-display: block; }
@font-face { font-family: "CV"; src: url("arialbi.ttf") format("truetype"); font-weight: 700; font-style: italic; font-display: block; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  font-family: "CV", Arial, sans-serif;
  font-size: 10.5pt;
  line-height: 1.28;
  color: #000;
  background: #fff;
  font-synthesis: none;
  -webkit-font-smoothing: antialiased;
  print-color-adjust: exact;
  -webkit-print-color-adjust: exact;
}
.photo {
  float: right;
  width: 112pt;
  height: 140pt;
  object-fit: cover;
  object-position: 50% 18%;
  margin: 0 0 8pt 10pt;
}
h1 { font-size: 20pt; font-weight: 700; line-height: 1.1; margin: 0 0 3pt; }
.role-line { font-size: 11.5pt; font-weight: 700; margin: 0 0 5pt; }
.meta { font-size: 10pt; line-height: 1.35; margin-bottom: 1.5pt; }
a { color: #1155CC; text-decoration: underline; }
h2 {
  font-size: 11.5pt;
  font-weight: 700;
  margin: 9pt 0 4pt;
  clear: both;
  border-bottom: 0.6pt solid #222;
  padding-bottom: 2pt;
}
ul { margin: 0 0 3pt 16pt; padding: 0; }
li { margin: 0 0 2pt; }
.job { page-break-inside: avoid; break-inside: avoid; }
.company {
  font-weight: 700;
  font-style: italic;
  margin: 8pt 0 2pt;
  padding-left: 16pt;
  position: relative;
}
.company::before {
  content: "●";
  position: absolute;
  left: 3pt;
  font-style: normal;
  font-weight: 400;
}
.context { font-style: italic; margin: 0 0 3pt 16pt; }
.role { font-weight: 700; margin: 2pt 0 2pt 16pt; }
.intro { margin: 0 0 2pt 16pt; }
.label { font-weight: 700; margin: 3pt 0 2pt 16pt; }
.dates { white-space: nowrap; }
.chips { margin: 0 0 5pt; }
.chip { display: inline-block; margin: 0 4pt 2pt 0; padding: 1pt 6pt; border: 0.5pt solid #888; border-radius: 3pt; font-size: 9pt; }
"""

HTML_UK = f"""<!DOCTYPE html>
<html lang="uk">
<head><meta charset="UTF-8"><title>Денис Паршенцев — CV</title><style>{CSS}</style></head>
<body>
  <img class="photo" src="photo.png" alt="Денис Паршенцев">
  <h1>Денис Паршенцев</h1>
  <p class="role-line">Операційний директор (COO) · Head of E-commerce</p>
  <p class="chips"><span class="chip">Retail</span><span class="chip">E-commerce</span><span class="chip">Q-commerce</span><span class="chip">Логістика</span></p>
  <p class="meta"><b>Дніпро</b> · <a href="tel:+380503633127">+380 50 363 31 27</a> · <a href="mailto:parshencevdenis@gmail.com">parshencevdenis@gmail.com</a></p>
  <p class="meta"><a href="https://www.linkedin.com/in/denis-parshentsev/">linkedin.com/in/denis-parshentsev</a> · <a href="https://parshentsev-cv.vercel.app/site?lang=uk">Веб-візитка</a></p>

  <h2>Профіль</h2>
  <p>Керівник із досвідом в e-commerce та ритейлі з 2007 року: АЛЛО, VARUS, LOKO / Fozzy Group. Поєдную управління операціями та P&amp;L із розвитком цифрових продуктів, запуском каналів продажів і підвищенням ефективності бізнесу.</p>
  <p style="margin-top:4pt">Досвід охоплює операційну структуру зі 150+ працівниками, продуктову модель e-commerce, доставку й цифрові платформи, ERP та координацію масштабування сервісу до 64 міст.</p>

  <h2>Масштаб досвіду та результати</h2>
  <ul>
    <li><b>×16</b> — зростання обороту LOKO з квітня 2023 (результат бізнесу; особистий внесок — у досвіді).</li>
    <li><b>64 міста</b> — координація підтримки географічного масштабування з командами холдингу.</li>
    <li><b>150+</b> — операційна структура АЛЛО-online (філії, склади, видача, доставка), 2012–2016.</li>
    <li><b>До 90%</b> — доступність цільових та пенетраційних артикулів у LOKO.</li>
    <li><b>ERP</b> — Oracle JD Edwards з боку бізнесу: процеси, облік, перехід і звірки.</li>
  </ul>

  <h2>Цільові позиції</h2>
  <ul>
    <li>Операційний директор (COO)</li>
    <li>Директор з електронної комерції (Head of E-commerce)</li>
    <li>Директор з розвитку бізнесу (CBDO)</li>
    <li>CEO невеликого бізнесу</li>
  </ul>

  <h2>Управлінська експертиза</h2>
  <ul>
    <li><b>Операції:</b> збирання замовлень, склади, видача, власна/партнерська доставка, клієнтський сервіс.</li>
    <li><b>Фінанси:</b> бюджетування, P&amp;L, звітність, юніт-економіка, інвестиційні кейси.</li>
    <li><b>Люди та процеси:</b> керівники напрямів, KPI, регламенти, міжфункціональна взаємодія.</li>
    <li><b>Цифрова трансформація:</b> платформи й застосунки, продуктові команди, ROPO, Oracle JD Edwards.</li>
    <li><b>Розвиток бізнесу:</b> агрегатори, партнерства, географія й асортимент, нові канали.</li>
  </ul>

  <h2>Досвід</h2>

  <div class="job">
  <p class="company">LOKO (Fozzy Group)<span class="dates"> | Квітень 2023 — дотепер</span></p>
  <p class="role">Заступник керівника LOKO з питань стратегічних проєктів та партнерств</p>
  <p class="intro">Ініціативи зростання й ефективності продуктового напряму; управління напрямом агрегаторів, включно з бюджетуванням і продажами. Пряма команда менеджерів і координація підрозділів холдингу.</p>
  <p class="label">Результати:</p>
  <ul>
    <li>Запуск і розвиток каналу Glovo / Bolt Food: модель, домовленості, процеси, KPI напряму.</li>
    <li>Координація з операціями й маркетингом холдингу під час розширення до 64 міст.</li>
    <li>Розширення асортименту з торгових залів офлайн-філій; доступність цільових і пенетраційних артикулів до 90%.</li>
    <li>Ініціативи економіки: пороги доставки, динамічні тарифи, пакування, сервісні збори, двоетапна оплата (ефект на EBITDA — NDA).</li>
    <li>Бізнесові та юридичні схеми для нових напрямів, зокрема ліків, разом із юридичною службою та партнерами.</li>
  </ul>
  </div>

  <div class="job">
  <p class="company">VARUS Ecommerce<span class="dates"> | 2020 — 2023</span></p>
  <p class="role">Заступник директора з електронної комерції / операційний директор (COO)</p>
  <p class="intro">Операційна модель e-commerce; 4–5 керівників напрямів; P&amp;L дирекції. IT/маркетинг — на окремих етапах; комерція поділена з холдингом. Готував і захищав інвестиційні рішення перед комітетами холдингу.</p>
  <p class="label">Результати:</p>
  <ul>
    <li>Бізнесова й фінансова моделі розвитку після аудиту; побудова операційних процесів.</li>
    <li>Тендери та захист рішень на рівні холдингу; бюджетування поточних витрат у межах повноважень.</li>
    <li>Запуск нової e-commerce платформи та власної доставки з профільними командами й підрядниками.</li>
    <li>Процес збирання замовлень і протоколи взаємодії з операційною командою мережі.</li>
    <li>Підготував інвестиційний кейс великого даркстору (модель, інфраструктура, розрахунки).</li>
  </ul>
  </div>

  <div class="job">
  <p class="company">Група компаній АЛЛО<span class="dates"> | 2007 — 2020</span></p>
  <p class="role">Керівник онлайн-напряму / керівник відділу розвитку бізнесу АЛЛО-online<span class="dates"> | 2016 — 2020</span></p>
  <p class="intro">Розвиток цифрових платформ, продуктові метрики та бюджети команд і розробки. Управління продуктовою командою, проєктними менеджерами, дизайнерами, QA та зовнішніми командами.</p>
  <ul>
    <li>Розвиток сайту й застосунку; продуктова підтримка KPI онлайн-каналу.</li>
    <li>Початковий етап платформи маркетплейсу: вимоги, пріоритети, координація команд.</li>
    <li>ROPO-аналітика: зв’язок онлайн-взаємодій із покупками в мережі.</li>
  </ul>
  <p class="role">Керівник відділу продажів АЛЛО-online<span class="dates"> | 2012 — 2016</span></p>
  <p class="intro">Операційна структура 150+ працівників; директори філій і сервісні керівники в прямому підпорядкуванні.</p>
  <ul>
    <li>Мережа філій і виконання замовлень: обробка, видача, власна доставка, перевізники, післяпродажне обслуговування.</li>
    <li>Склади, облік, переобліки; ТЗ для IT, регламенти, KPI та мотивація.</li>
  </ul>
  <p class="role">Директор Дніпропетровської філії інтернет-магазину<span class="dates"> | 2007 — 2012</span></p>
  <ul>
    <li>Філія з нуля: персонал, процеси, витрати; далі — підвищення на національний рівень.</li>
  </ul>
  <p class="role">Окремий проєкт — впровадження Oracle JD Edwards (у межах АЛЛО)</p>
  <p class="intro">Участь у впровадженні Oracle JD Edwards з боку бізнесу.</p>
  <ul>
    <li>Вимоги, ТЗ, логіка операцій, сервісу й обліку; паралельні системи, звірки, запуск на філіях, взаємодія з КРУ.</li>
  </ul>
  </div>

  <div class="job">
  <p class="company">Ранній досвід<span class="dates"> | 2005 — 2007</span></p>
  <ul>
    <li>ФОП (2006–2007): GPS-моніторинг транспорту. Плей Мобайл Технолоджі (2005–2007): B2B мобільний зв’язок.</li>
  </ul>
  </div>

  <h2>Освіта та розвиток</h2>
  <ul>
    <li><b>Незавершена вища освіта:</b> фізика; економіка підприємств.</li>
    <li><b>U Open University:</b> управління проєктами (Lic. UOU2018032503).</li>
    <li><b>Управлінські програми:</b> лідерство, корпоративна культура, бізнес-комунікації (А. Станченко, В. Давтян та ін.).</li>
    <li><b>Англійська:</b> B2 / Upper-Intermediate.</li>
  </ul>
</body>
</html>
"""

HTML_EN = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Denis Parshentsev — CV</title><style>{CSS}</style></head>
<body>
  <img class="photo" src="photo.png" alt="Denis Parshentsev">
  <h1>Denis Parshentsev</h1>
  <p class="role-line">Chief Operating Officer (COO) · Head of E-commerce</p>
  <p class="chips"><span class="chip">Retail</span><span class="chip">E-commerce</span><span class="chip">Q-commerce</span><span class="chip">Logistics</span></p>
  <p class="meta"><b>Dnipro</b> · <a href="tel:+380503633127">+380 50 363 31 27</a> · <a href="mailto:parshencevdenis@gmail.com">parshencevdenis@gmail.com</a></p>
  <p class="meta"><a href="https://www.linkedin.com/in/denis-parshentsev/">linkedin.com/in/denis-parshentsev</a> · <a href="https://parshentsev-cv.vercel.app/site?lang=en">Web CV</a></p>

  <h2>Profile</h2>
  <p>Operator and product leader in e-commerce and retail since 2007: ALLO, VARUS, LOKO / Fozzy Group. I combine operations and P&amp;L ownership with digital product development, channel launches and business efficiency.</p>
  <p style="margin-top:4pt">Experience covers an operating structure of 150+ people, product-led e-commerce, delivery and platforms, ERP from the business side, and coordinated scaling to 64 cities.</p>

  <h2>Scale of experience and results</h2>
  <ul>
    <li><b>×16</b> — LOKO turnover growth from April 2023 (business outcome; personal contribution in Experience).</li>
    <li><b>64 cities</b> — coordinated geographic scale-up with holding operations and marketing.</li>
    <li><b>150+</b> — ALLO-online operating structure (branches, warehouses, pickup, delivery), 2012–2016.</li>
    <li><b>Up to 90%</b> — availability of target and penetration SKUs in LOKO.</li>
    <li><b>ERP</b> — Oracle JD Edwards business-side rollout: processes, accounting, cutover, reconciliations.</li>
  </ul>

  <h2>Target positions</h2>
  <ul>
    <li>Chief Operating Officer (COO)</li>
    <li>Head of E-commerce / E-commerce Director</li>
    <li>Chief Business Development Officer (CBDO)</li>
    <li>CEO of a small business</li>
  </ul>

  <h2>Management expertise</h2>
  <ul>
    <li><b>Operations:</b> picking, warehouses, pickup, owned/partner delivery, customer service.</li>
    <li><b>Finance:</b> budgeting, P&amp;L, reporting, unit economics, investment cases.</li>
    <li><b>People &amp; process:</b> function leads, KPI, playbooks, cross-functional orchestration.</li>
    <li><b>Digital:</b> platforms and apps, product teams, ROPO, Oracle JD Edwards.</li>
    <li><b>Business development:</b> aggregators, partnerships, geography and assortment, new channels.</li>
  </ul>

  <h2>Experience</h2>

  <div class="job">
  <p class="company">LOKO (Fozzy Group)<span class="dates"> | April 2023 — present</span></p>
  <p class="role">Deputy Head of LOKO, Strategic Projects &amp; Partnerships</p>
  <p class="intro">Growth and efficiency initiatives for the grocery line; owned the aggregators stream including budgeting and sales. Led a team of managers and coordinated holding functions.</p>
  <p class="label">Results:</p>
  <ul>
    <li>Launched Glovo / Bolt Food channel: model, terms, processes, stream KPIs.</li>
    <li>Coordinated with holding ops and marketing during expansion to 64 cities.</li>
    <li>Expanded the offer using in-store assortment from offline branches; up to 90% availability of target/penetration SKUs.</li>
    <li>Implemented profitability improvement initiatives: delivery thresholds, dynamic tariffs, packaging, service fees, two-step payment (EBITDA effect under NDA).</li>
    <li>Commercial and legal schemes for new streams, including medicines, with the legal team and partners.</li>
  </ul>
  </div>

  <div class="job">
  <p class="company">VARUS Ecommerce<span class="dates"> | 2020 — 2023</span></p>
  <p class="role">Deputy Director of E-commerce / Chief Operating Officer (COO)</p>
  <p class="intro">E-commerce operating model; 4–5 function leads; directorate P&amp;L. IT/marketing at selected stages; commerce shared with the holding. Prepared and justified investment proposals before holding committees.</p>
  <p class="label">Results:</p>
  <ul>
    <li>Business and financial development models after audit; operating processes.</li>
    <li>Tenders and presented business/technology proposals at holding level; day-to-day spend within mandate.</li>
    <li>New e-commerce platform and owned delivery with specialist teams and vendors.</li>
    <li>Order-picking process and e-commerce ↔ store-ops protocols.</li>
    <li>Prepared a large dark-store investment case (ops model, infrastructure, finance).</li>
  </ul>
  </div>

  <div class="job">
  <p class="company">ALLO Group<span class="dates"> | 2007 — 2020</span></p>
  <p class="role">Head of Online / Head of Business Development, ALLO-online<span class="dates"> | 2016 — 2020</span></p>
  <p class="intro">Digital platform development, product metrics and engineering budgets. Led product, PMs, design, QA and external engineering teams.</p>
  <ul>
    <li>Website and app development; product support for online-channel KPIs.</li>
    <li>Early marketplace platform: requirements, priorities, team coordination.</li>
    <li>ROPO analytics linking online interactions to in-store purchases.</li>
  </ul>
  <p class="role">Head of ALLO-online Sales<span class="dates"> | 2012 — 2016</span></p>
  <p class="intro">Operating structure of 150+ people; branch directors and service leads in direct line.</p>
  <ul>
    <li>Branch network and fulfillment: processing, pickup, owned delivery, carriers, after-sales service.</li>
    <li>Warehouses and stock control; IT specs, playbooks, KPI and incentives.</li>
  </ul>
  <p class="role">Director, Dnipro internet-store branch<span class="dates"> | 2007 — 2012</span></p>
  <ul>
    <li>Built the branch from scratch; later promoted to national ALLO-online leadership.</li>
  </ul>
  <p class="role">Separate project — Oracle JD Edwards (within ALLO)</p>
  <p class="intro">Business-side participation in the Oracle JD Edwards rollout.</p>
  <ul>
    <li>Requirements, specs, ops/service/accounting logic; parallel systems, reconciliations, branch go-live, work with internal audit.</li>
  </ul>
  </div>

  <div class="job">
  <p class="company">Earlier career<span class="dates"> | 2005 — 2007</span></p>
  <ul>
    <li>Private entrepreneur (2006–2007): GPS fleet monitoring. Play Mobile Technology (2005–2007): B2B mobile telecom.</li>
  </ul>
  </div>

  <h2>Education &amp; development</h2>
  <ul>
    <li><b>Incomplete higher education:</b> Physics; Enterprise Economics.</li>
    <li><b>U Open University:</b> project management (Lic. UOU2018032503).</li>
    <li><b>Executive programs:</b> leadership, corporate culture, business communications (A. Stanchenko, V. Davtyan, et al.).</li>
    <li><b>English:</b> B2 / Upper-Intermediate.</li>
  </ul>
</body>
</html>
"""


def prepare_build() -> None:
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir()
    shutil.copy(ROOT / "photo.png", BUILD / "photo.png")
    for dest, src_name in FONT_FILES.items():
        src = FONTS / src_name
        if not src.exists():
            raise FileNotFoundError(f"Missing font: {src}")
        shutil.copy(src, BUILD / dest)
    (BUILD / "cv-uk.html").write_text(HTML_UK, encoding="utf-8")
    (BUILD / "cv-en.html").write_text(HTML_EN, encoding="utf-8")


def print_pdf(html_path: Path, pdf_path: Path) -> None:
    with sync_playwright() as p:
        browser = None
        last_error = None
        for channel in ("chrome", "msedge"):
            try:
                browser = p.chromium.launch(channel=channel, headless=True)
                break
            except Exception as exc:  # noqa: BLE001
                last_error = exc
        if browser is None:
            raise RuntimeError(f"Could not launch Chrome/Edge: {last_error}")
        page = browser.new_page()
        page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
        page.evaluate("() => document.fonts.ready")
        page.wait_for_timeout(250)
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={"top": "10mm", "bottom": "10mm", "left": "12mm", "right": "12mm"},
        )
        browser.close()


def copy_with_retry(src: Path, dst: Path) -> None:
    last_error: Exception | None = None
    for _ in range(5):
        try:
            shutil.copyfile(src, dst)
            return
        except PermissionError as exc:
            last_error = exc
            time.sleep(0.5)
    raise PermissionError(
        f"Cannot overwrite {dst.name}. Close it in Acrobat or another viewer, then run again."
    ) from last_error


def main() -> int:
    prepare_build()
    print_pdf(BUILD / "cv-uk.html", BUILD / "cv.pdf")
    print_pdf(BUILD / "cv-en.html", BUILD / "cv-en.pdf")
    copy_with_retry(BUILD / "cv.pdf", OUT_UK)
    copy_with_retry(BUILD / "cv-en.pdf", OUT_EN)
    time.sleep(0.3)
    shutil.rmtree(BUILD, ignore_errors=True)
    print(f"Wrote {OUT_UK.name} ({OUT_UK.stat().st_size // 1024} KB)")
    print(f"Wrote {OUT_EN.name} ({OUT_EN.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
