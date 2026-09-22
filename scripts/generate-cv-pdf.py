"""Generate UA + EN executive CV PDFs (3-page, source-driven)."""
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
  font-size: 10.75pt;
  line-height: 1.4;
  color: #111;
  background: #fff;
  font-synthesis: none;
  -webkit-font-smoothing: antialiased;
  print-color-adjust: exact;
  -webkit-print-color-adjust: exact;
}
a { color: #1d4ed8; text-decoration: none; }
.header {
  display: grid;
  grid-template-columns: 1fr 74pt;
  gap: 10pt 14pt;
  align-items: start;
  margin-bottom: 10pt;
}
.header__text { min-width: 0; }
.photo {
  width: 74pt;
  height: 94pt;
  object-fit: cover;
  object-position: 50% 18%;
  border-radius: 2pt;
}
h1 {
  font-size: 27pt;
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -0.02em;
  margin: 0 0 3pt;
  color: #0a0a0a;
}
.role-line {
  font-size: 12pt;
  font-weight: 700;
  color: #1d4ed8;
  margin: 0 0 6pt;
  line-height: 1.25;
}
.meta { font-size: 10pt; line-height: 1.45; color: #222; margin: 0 0 1.5pt; }
.skills-line {
  margin-top: 7pt;
  font-size: 9.75pt;
  color: #333;
  line-height: 1.35;
}
h2 {
  font-size: 13.5pt;
  font-weight: 700;
  margin: 11pt 0 5pt;
  color: #0a0a0a;
  border-bottom: 1.1pt solid #1d4ed8;
  padding-bottom: 2pt;
}
.profile p { margin: 0 0 5pt; }
.metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6pt;
  margin: 8pt 0 2pt;
}
.metric {
  border: 0.7pt solid #cbd5e1;
  border-radius: 3pt;
  padding: 6pt 7pt;
  background: #f8fafc;
}
.metric__value {
  display: block;
  font-size: 12.5pt;
  font-weight: 700;
  color: #1d4ed8;
  line-height: 1.15;
  margin-bottom: 2pt;
}
.metric__desc { font-size: 8.75pt; line-height: 1.3; color: #334155; }
.job { margin: 0 0 11pt; }
.job--keep { page-break-inside: avoid; break-inside: avoid; }
.job--page { page-break-before: always; break-before: page; }
.company {
  font-size: 15.5pt;
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 1pt;
  color: #0a0a0a;
}
.dates {
  display: block;
  font-size: 9.75pt;
  font-weight: 400;
  color: #475569;
  margin: 0 0 4pt;
}
.role {
  font-size: 11.25pt;
  font-weight: 700;
  margin: 0 0 3pt;
  line-height: 1.3;
}
.intro { margin: 0 0 4pt; }
ul { margin: 0 0 0 13pt; padding: 0; }
li { margin: 0 0 3.5pt; padding-left: 1pt; }
li b { font-weight: 700; }
.role-block { margin: 14pt 0 0; padding-top: 8pt; }
.role-block:first-of-type { margin-top: 2pt; padding-top: 0; }
.project {
  margin-top: 10pt;
  padding-top: 7pt;
  border-top: 0.6pt solid #e2e8f0;
}
.compact p, .compact li { margin-bottom: 2.5pt; }
.compact h2 { margin-top: 10pt; }
"""

HTML_UK = f"""<!DOCTYPE html>
<html lang="uk">
<head><meta charset="UTF-8"><title>Денис Паршенцев — CV</title><style>{CSS}</style></head>
<body>
  <header class="header">
    <div class="header__text">
      <h1>Денис Паршенцев</h1>
      <p class="role-line">Операційний директор (COO) · Head of E-commerce</p>
      <p class="meta"><b>Дніпро</b> · <a href="tel:+380503633127">+380 50 363 31 27</a> · <a href="mailto:parshencevdenis@gmail.com">parshencevdenis@gmail.com</a></p>
      <p class="meta"><a href="https://www.linkedin.com/in/denis-parshentsev/">linkedin.com/in/denis-parshentsev</a> · <a href="https://parshentsev-cv.vercel.app/site?lang=uk">Веб-візитка</a></p>
      <p class="skills-line">Операції та P&amp;L · Розвиток e-commerce · Команди та процеси · Цифрова трансформація</p>
    </div>
    <img class="photo" src="photo.png" alt="Денис Паршенцев">
  </header>

  <h2>Профіль</h2>
  <div class="profile">
    <p>Керівник з досвідом розвитку e-commerce та управління операціями в АЛЛО, VARUS і LOKO / Fozzy Group. Поєдную бюджетування та управління P&amp;L із побудовою операційних моделей, розвитком цифрових продуктів і запуском каналів продажів. Керував операційною структурою зі 150+ працівниками та командами керівників напрямів. Мій досвід охоплює виконання замовлень, склади, доставку, клієнтський сервіс, продуктові команди та впровадження ERP з боку бізнесу. Сильна сторона — організація роботи між підрозділами та перетворення окремих ініціатив на керовані процеси з відповідальністю й показниками результату.</p>
  </div>

  <div class="metrics">
    <div class="metric">
      <span class="metric__value">64 міста</span>
      <span class="metric__desc">Географія LOKO; координація масштабування з командами холдингу</span>
    </div>
    <div class="metric">
      <span class="metric__value">150+ працівників</span>
      <span class="metric__desc">Операційна структура АЛЛО-online, 2012–2016</span>
    </div>
    <div class="metric">
      <span class="metric__value">4–5 керівників</span>
      <span class="metric__desc">Команда управління у VARUS Ecommerce</span>
    </div>
  </div>

  <h2>Досвід</h2>

  <section class="job job--keep">
    <p class="company">LOKO / Fozzy Group</p>
    <span class="dates">квітень 2023 — дотепер</span>
    <p class="role">Заступник керівника LOKO з питань стратегічних проєктів та партнерств</p>
    <p class="intro">Відповідаю за ініціативи зростання й підвищення ефективності продуктового напряму LOKO. Керую напрямом агрегаторів, включно з бюджетуванням і продажами, та командою менеджерів. Організовую взаємодію з операційною командою, маркетингом, юридичною службою та іншими напрямами холдингу.</p>
    <ul>
      <li><b>Новий канал продажів.</b> Запустив і розвиваю напрям агрегаторів: бізнес-модель, партнерські домовленості, операційні процеси та показники результативності.</li>
      <li><b>Географічне масштабування.</b> Координував взаємодію LOKO з операційною командою та маркетингом холдингу під час розширення сервісу до 64 міст.</li>
      <li><b>Асортимент і доступність.</b> Реалізував розширення пропозиції за рахунок асортименту торгових залів офлайн-філій. Асортимент збільшено в кілька разів, доступність цільових та пенетраційних артикулів — до 90%.</li>
      <li><b>Операційна ефективність.</b> Впровадив ініціативи щодо порогів доставки, динамічних тарифів, пакування, сервісних зборів і двоетапної оплати з вимірюваним позитивним впливом на EBITDA.</li>
      <li><b>Нові напрями продажів.</b> Розробляв і впроваджував бізнес-моделі та юридичні механізми для регульованих категорій, зокрема лікарських засобів, у взаємодії з юридичною службою та партнерами.</li>
    </ul>
  </section>

  <section class="job job--page job--keep">
    <p class="company">VARUS Ecommerce</p>
    <span class="dates">2020–2023</span>
    <p class="role">Заступник директора з електронної комерції / операційний директор</p>
    <p class="intro">Відповідав за побудову та розвиток операційної моделі e-commerce, бюджетування, управління P&amp;L і фінансову звітність напряму. У підпорядкуванні — 4–5 керівників напрямів. Керував збиранням замовлень, доставкою та клієнтським сервісом; на окремих етапах — також IT і маркетингом.</p>
    <ul>
      <li><b>Бізнесова та фінансова моделі.</b> Проаналізував стан e-commerce на початковому етапі розвитку й розробив моделі його подальшої роботи та масштабування.</li>
      <li><b>Платформа й доставка.</b> Разом із профільними командами та підрядниками запустив нову e-commerce платформу та власну доставку, побудувавши відповідні операційні процеси.</li>
      <li><b>Взаємодія з торговельною мережею.</b> Організував процес збирання замовлень і розробив протоколи взаємодії e-commerce з операційною командою мережі.</li>
      <li><b>Фінанси та інвестиційні рішення.</b> Вів бюджетування і підготовку фінансової звітності, готував тендери та захищав бізнесові й IT-рішення перед комітетами холдингу.</li>
      <li><b>Планування інфраструктури.</b> Підготував інвестиційний кейс великого даркстору: операційну модель, вимоги до інфраструктури та фінансові розрахунки.</li>
    </ul>
  </section>

  <section class="job job--keep">
    <p class="company">АЛЛО</p>
    <span class="dates">2016–2020</span>
    <p class="role">Керівник онлайн-напряму / керівник відділу розвитку бізнесу АЛЛО-online</p>
    <p class="intro">Відповідав за розвиток цифрових платформ, продуктові метрики та бюджети команд і розробки. Керував продуктовою командою, проєктними менеджерами, дизайнерами й QA; координував роботу зовнішніх команд розробки.</p>
    <ul>
      <li><b>Сайт і мобільний застосунок.</b> Організовував розвиток продуктів і виконання продуктових завдань, що підтримували бізнес-показники онлайн-каналу.</li>
      <li><b>Платформа маркетплейсу.</b> Керував продуктовою роботою на початковому етапі розвитку платформи: вимоги, пріоритети та взаємодія команд.</li>
      <li><b>ROPO-аналітика.</b> Впровадив аналітику зв’язку між онлайн-взаємодіями та покупками у фізичних магазинах.</li>
    </ul>
  </section>

  <section class="job job--keep">
    <p class="company">АЛЛО-online</p>
    <span class="dates">2012–2016</span>
    <p class="role">Керівник відділу продажів</p>
    <p class="intro">Керував операційною структурою зі 150+ працівниками, включно з філіями, складами, точками видачі та кур’єрами. У прямому підпорядкуванні — директори філій і керівники сервісних підрозділів.</p>
    <ul>
      <li><b>Повний цикл виконання замовлення.</b> Організовував обробку, видачу, власну доставку та роботу з перевізниками, клієнтську підтримку й післяпродажне обслуговування.</li>
      <li><b>Складські операції.</b> Відповідав за роботу власних складів, облік і переобліки, взаємодію з логістикою та приймання товарів від клієнтів.</li>
      <li><b>Розвиток мережі.</b> Будував процеси роботи філій; організовував перевірку нових рішень у підпорядкованих підрозділах перед масштабуванням.</li>
      <li><b>Автоматизація та управління результативністю.</b> Формував ТЗ для IT, впроваджував регламенти, KPI та системи мотивації; планував діяльність і витрати підрозділів.</li>
    </ul>
  </section>

  <section class="job job--page job--keep">
    <p class="company">АЛЛО</p>
    <span class="dates">2007–2012</span>
    <p class="role">Директор Дніпропетровської філії інтернет-магазину</p>
    <p class="intro">Побудував роботу філії з нуля: підбір команди, операційні процеси, планування витрат, мотивація персоналу та взаємодія зі службами компанії. Надалі перейшов до управління операціями АЛЛО-online на національному рівні.</p>

    <div class="project">
      <p class="role">Окремий проєкт у межах АЛЛО: Oracle JD Edwards</p>
      <p class="intro">Брав участь у впровадженні ERP з боку бізнесу, пов’язуючи вимоги онлайн-продажів і сервісу з процесами фінансового обліку.</p>
      <ul>
        <li>Формував бізнес-вимоги та технічні завдання, опрацьовував логіку операцій, сервісу, обліку й звірок.</li>
        <li>Брав участь у переході між системами: паралельне ведення операцій, узгодження даних та усунення розбіжностей.</li>
        <li>Супроводжував запуск на філіях, зведення й звірку даних у тісній взаємодії з контрольно-ревізійним управлінням.</li>
      </ul>
    </div>
  </section>

  <section class="compact">
    <h2>Ранній досвід</h2>
    <ul>
      <li>Приватний підприємець (2006–2007): продаж і впровадження GPS-моніторингу автотранспорту.</li>
      <li>ТОВ «Плей Мобайл Технолоджі» (2005–2007): корпоративні продажі мобільного зв’язку та залучення B2B-клієнтів.</li>
    </ul>

    <h2>Освіта та розвиток</h2>
    <ul>
      <li><b>Незавершена вища освіта:</b> фізика; економіка підприємств.</li>
      <li><b>U Open University:</b> управління проєктами (Lic. UOU2018032503).</li>
      <li><b>Управлінські програми:</b> лідерство, корпоративна культура, бізнес-комунікації (А. Станченко, В. Давтян та ін.).</li>
      <li><b>Англійська:</b> B2 / Upper-Intermediate.</li>
    </ul>
  </section>
</body>
</html>
"""

HTML_EN = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Denis Parshentsev — CV</title><style>{CSS}</style></head>
<body>
  <header class="header">
    <div class="header__text">
      <h1>Denis Parshentsev</h1>
      <p class="role-line">Chief Operating Officer (COO) · Head of E-commerce</p>
      <p class="meta"><b>Dnipro</b> · <a href="tel:+380503633127">+380 50 363 31 27</a> · <a href="mailto:parshencevdenis@gmail.com">parshencevdenis@gmail.com</a></p>
      <p class="meta"><a href="https://www.linkedin.com/in/denis-parshentsev/">linkedin.com/in/denis-parshentsev</a> · <a href="https://parshentsev-cv.vercel.app/site?lang=en">Web CV</a></p>
      <p class="skills-line">Operations &amp; P&amp;L · E-commerce growth · Teams &amp; processes · Digital transformation</p>
    </div>
    <img class="photo" src="photo.png" alt="Denis Parshentsev">
  </header>

  <h2>Profile</h2>
  <div class="profile">
    <p>Operations and digital product leader with experience building e-commerce and running operations at ALLO, VARUS and LOKO / Fozzy Group. I combine budgeting and P&amp;L management with operating-model design, digital product development and sales-channel launches. I have led an operating structure of 150+ people and teams of function leads. My experience covers order fulfillment, warehouses, delivery, customer service, product teams and business-side ERP rollout. Strength: organizing cross-functional work and turning discrete initiatives into managed processes with clear ownership and performance metrics.</p>
  </div>

  <div class="metrics">
    <div class="metric">
      <span class="metric__value">64 cities</span>
      <span class="metric__desc">LOKO geography; coordinated scale-up with holding teams</span>
    </div>
    <div class="metric">
      <span class="metric__value">150+ people</span>
      <span class="metric__desc">ALLO-online operating structure, 2012–2016</span>
    </div>
    <div class="metric">
      <span class="metric__value">4–5 function heads</span>
      <span class="metric__desc">Management team at VARUS Ecommerce</span>
    </div>
  </div>

  <h2>Experience</h2>

  <section class="job job--keep">
    <p class="company">LOKO / Fozzy Group</p>
    <span class="dates">April 2023 — present</span>
    <p class="role">Deputy Head of LOKO, Strategic Projects &amp; Partnerships</p>
    <p class="intro">I drive growth and efficiency initiatives for LOKO’s grocery line. I am responsible for aggregator partnerships, budgeting and sales, and lead a team of managers. I coordinate work with operations, marketing, legal and other holding functions.</p>
    <ul>
      <li><b>New sales channel.</b> Launched and continue to develop the aggregators stream: business model, partner terms, operating processes and performance metrics.</li>
      <li><b>Geographic scale-up.</b> Coordinated LOKO with holding operations and marketing while expanding the service to 64 cities.</li>
      <li><b>Assortment and availability.</b> Expanded the offer using assortment from physical stores. Assortment grew several times; availability of target and penetration SKUs reached up to 90%.</li>
      <li><b>Operating efficiency.</b> Implemented delivery thresholds, dynamic tariffs, packaging, service fees and two-step payment with a measurable positive impact on EBITDA.</li>
      <li><b>New sales streams.</b> Developed and rolled out business models and legal frameworks for regulated categories, including medicines, with the legal team and partners.</li>
    </ul>
  </section>

  <section class="job job--page job--keep">
    <p class="company">VARUS Ecommerce</p>
    <span class="dates">2020–2023</span>
    <p class="role">Deputy Director of E-commerce / Chief Operating Officer</p>
    <p class="intro">Built and developed the e-commerce operating model, budgeting, P&amp;L management and financial reporting for the unit. Managed 4–5 department heads. Owned picking, delivery and customer service; at selected stages also IT and marketing.</p>
    <ul>
      <li><b>Business and financial models.</b> Assessed e-commerce at an early stage and designed models for operating and scaling the unit.</li>
      <li><b>Platform and delivery.</b> With specialist teams and vendors, launched a new e-commerce platform and in-house delivery, building the matching operating processes.</li>
      <li><b>Store-network collaboration.</b> Set up order picking and designed e-commerce interaction protocols with the retail network’s operations team.</li>
      <li><b>Finance and investment decisions.</b> Ran budgeting and financial reporting, managed tenders and presented business and technology investment proposals to group committees.</li>
      <li><b>Infrastructure planning.</b> Prepared a large dark-store investment case: operating model, infrastructure requirements and financial calculations.</li>
    </ul>
  </section>

  <section class="job job--keep">
    <p class="company">ALLO</p>
    <span class="dates">2016–2020</span>
    <p class="role">Head of Online / Head of Business Development, ALLO-online</p>
    <p class="intro">Owned digital platform development, product metrics and team/engineering budgets. Led the product team, project managers, designers and QA; coordinated external engineering teams.</p>
    <ul>
      <li><b>Website and mobile app.</b> Organized product development and product work that supported online-channel business KPIs.</li>
      <li><b>Marketplace platform.</b> Led product work at the early stage of the marketplace platform: requirements, priorities and team collaboration.</li>
      <li><b>ROPO analytics.</b> Introduced analytics linking online interactions to purchases in physical stores.</li>
    </ul>
  </section>

  <section class="job job--keep">
    <p class="company">ALLO-online</p>
    <span class="dates">2012–2016</span>
    <p class="role">Head of Sales</p>
    <p class="intro">Led an operating structure of 150+ people across branches, warehouses, pickup points and couriers. Branch directors and service leads reported directly.</p>
    <ul>
      <li><b>End-to-end order fulfillment.</b> Organized processing, pickup, in-house delivery and carrier work, customer support and after-sales service.</li>
      <li><b>Warehouse operations.</b> Owned in-house warehouses, stock control and recounts, logistics interfaces and customer returns.</li>
      <li><b>Network development.</b> Built branch operating processes and piloted new solutions in reporting units before scaling.</li>
      <li><b>Automation and performance management.</b> Wrote IT specs, introduced playbooks, KPIs and incentive systems; planned unit activity and spend.</li>
    </ul>
  </section>

  <section class="job job--page job--keep">
    <p class="company">ALLO</p>
    <span class="dates">2007–2012</span>
    <p class="role">Director, Dnipro internet-store branch</p>
    <p class="intro">Built the branch from scratch: team hiring, operating processes, cost planning, staff incentives and interfaces with company services. Later moved into national ALLO-online operations leadership.</p>

    <div class="project">
      <p class="role">Separate project within ALLO: Oracle JD Edwards</p>
      <p class="intro">Participated in the ERP rollout from the business side, connecting online sales and service requirements with financial accounting processes.</p>
      <ul>
        <li>Defined business requirements and technical specs; worked through ops, service, accounting and reconciliation logic.</li>
        <li>Took part in system cutover: parallel operations, data alignment and resolving discrepancies.</li>
        <li>Supported branch go-live and data consolidation in close collaboration with internal audit / internal control.</li>
      </ul>
    </div>
  </section>

  <section class="compact">
    <h2>Earlier career</h2>
    <ul>
      <li>Private entrepreneur (2006–2007): sales and rollout of GPS fleet monitoring.</li>
      <li>Play Mobile Technology LLC (2005–2007): B2B mobile telecom sales and corporate client acquisition.</li>
    </ul>

    <h2>Education &amp; development</h2>
    <ul>
      <li><b>Incomplete higher education:</b> Physics; Enterprise Economics.</li>
      <li><b>U Open University:</b> project management (Lic. UOU2018032503).</li>
      <li><b>Executive programs:</b> leadership, corporate culture, business communications (A. Stanchenko, V. Davtyan, et al.).</li>
      <li><b>English:</b> B2 / Upper-Intermediate.</li>
    </ul>
  </section>
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


def print_pdf(html_path: Path, pdf_path: Path, footer_name: str) -> None:
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
            display_header_footer=True,
            header_template="<span></span>",
            footer_template=(
                f'<div style="font-size:8.5pt;width:100%;padding:0 16mm;color:#64748b;'
                f'font-family:Arial,sans-serif;display:flex;justify-content:space-between;">'
                f"<span>{footer_name}</span>"
                f'<span><span class="pageNumber"></span> / <span class="totalPages"></span></span>'
                f"</div>"
            ),
            margin={"top": "16mm", "bottom": "18mm", "left": "17mm", "right": "17mm"},
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
    print_pdf(BUILD / "cv-uk.html", BUILD / "cv.pdf", "Денис Паршенцев")
    print_pdf(BUILD / "cv-en.html", BUILD / "cv-en.pdf", "Denis Parshentsev")
    copy_with_retry(BUILD / "cv.pdf", OUT_UK)
    copy_with_retry(BUILD / "cv-en.pdf", OUT_EN)
    time.sleep(0.3)
    shutil.rmtree(BUILD, ignore_errors=True)
    print(f"Wrote {OUT_UK.name} ({OUT_UK.stat().st_size // 1024} KB)")
    print(f"Wrote {OUT_EN.name} ({OUT_EN.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
