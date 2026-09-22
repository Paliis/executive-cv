"""Typeset the existing Google Doc CV into PDF with one Unicode font.

Keeps the original document structure (not a new layout). Fixes mixed
Arial/Calibri Latin-vs-Cyrillic and missing Type3 company bullets.
"""
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

HTML = r"""<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <title>Денис Паршенцев — CV</title>
  <style>
    @font-face {
      font-family: "CV";
      src: url("arial.ttf") format("truetype");
      font-weight: 400;
      font-style: normal;
      font-display: block;
    }
    @font-face {
      font-family: "CV";
      src: url("arialbd.ttf") format("truetype");
      font-weight: 700;
      font-style: normal;
      font-display: block;
    }
    @font-face {
      font-family: "CV";
      src: url("ariali.ttf") format("truetype");
      font-weight: 400;
      font-style: italic;
      font-display: block;
    }
    @font-face {
      font-family: "CV";
      src: url("arialbi.ttf") format("truetype");
      font-weight: 700;
      font-style: italic;
      font-display: block;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    html, body {
      font-family: "CV", Arial, sans-serif;
      font-size: 13pt;
      line-height: 1.32;
      color: #000;
      background: #fff;
      font-synthesis: none;
      -webkit-font-smoothing: antialiased;
      print-color-adjust: exact;
      -webkit-print-color-adjust: exact;
    }

    .photo {
      float: right;
      width: 187pt;
      height: 250pt;
      object-fit: cover;
      object-position: 50% 18%;
      margin: 0 0 12pt 14pt;
    }

    h1 {
      font-size: 30pt;
      font-weight: 700;
      line-height: 1.12;
      margin: 0 0 10pt;
    }

    .meta {
      font-size: 14pt;
      line-height: 1.4;
      margin-bottom: 3pt;
    }

    a {
      color: #1155CC;
      text-decoration: underline;
    }

    h2 {
      font-size: 15pt;
      font-weight: 700;
      margin: 16pt 0 8pt;
      clear: none;
    }

    h2.block { clear: both; padding-top: 4pt; }

    ul {
      margin: 0 0 6pt 22pt;
      padding: 0;
    }
    li { margin: 0 0 3.5pt; }

    .company {
      font-weight: 700;
      font-style: italic;
      margin: 18pt 0 5pt 0;
      padding-left: 22pt;
      position: relative;
    }
    .company::before {
      content: "●";
      position: absolute;
      left: 5pt;
      font-style: normal;
      font-weight: 400;
    }

    .context {
      font-style: italic;
      margin: 0 0 7pt 22pt;
    }

    .role {
      font-weight: 700;
      font-style: italic;
      margin: 14pt 0 5pt 22pt;
    }

    .role .dates {
      white-space: nowrap;
    }

    .context + .role {
      margin-top: 2pt;
    }

    ul + .role {
      margin-top: 20pt;
    }

    .intro { margin: 0 0 6pt 22pt; }

    .label {
      font-weight: 700;
      margin: 11pt 0 5pt 22pt;
    }

    .extra-title {
      font-weight: 700;
      font-size: 14pt;
      margin: 18pt 0 8pt;
    }

    .company .dates {
      white-space: nowrap;
    }
  </style>
</head>
<body>
  <img class="photo" src="photo.png" alt="Денис Паршенцев">

  <h1>Денис Паршенцев</h1>
  <p class="meta"><b>25.11.1981</b></p>
  <p class="meta"><b>Місто:</b> Дніпро</p>
  <p class="meta"><b>Телефон:</b> +380 50 363 31 27</p>
  <p class="meta"><b>Email:</b> <a href="mailto:parshencevdenis@gmail.com">parshencevdenis@gmail.com</a></p>
  <p class="meta"><b>LinkedIn:</b> <a href="https://www.linkedin.com/in/denis-parshentsev/">linkedin.com/in/denis-parshentsev/</a></p>
  <p class="meta"><a href="https://parshentsev-cv.vercel.app/site?lang=uk"><b>Веб-візитка</b></a></p>

  <h2>Експертна спеціалізація (Сфери діяльності):</h2>
  <ul>
    <li><b>E-commerce &amp; Q-commerce</b> (управління Highload цифровими екосистемами).</li>
    <li><b>Retail</b> (трансформація класичного ритейлу в Omnichannel).</li>
    <li><b>IT / Digital Products</b> (управління продуктовими командами та запуск систем з нуля).</li>
    <li><b>Логістика та Supply Chain</b> (оптимізація останньої милі, фулфілменту та Dark Store інфраструктури).</li>
  </ul>

  <h2>Цільові позиції:</h2>
  <ul>
    <li>Генеральний директор (CEO)</li>
    <li>Операційний директор (COO)</li>
    <li>Директор з електронної комерції (Head of E-commerce / E-commerce Director)</li>
    <li>Директор з розвитку бізнесу (Chief Business Development Officer / CBDO)</li>
  </ul>

  <h2 class="block">Досвід:</h2>

  <p class="company">LOKO (Fozzy Group)<span class="dates"> | Квітень 2023 — дотепер</span></p>
  <p class="context">Контекст: Q-commerce екосистема у складі найбільшого продуктового ритейлера України.</p>
  <p class="role">Заступник керівника LOKO з питань стратегічних проєктів та партнерств<span class="dates"> | Квітень 2023 — дотепер</span></p>
  <ul>
    <li>Стратегічне управління, фінансове планування, бюджетування та супровід продукту на етапі масштабування бізнес-платформи у 16 разів за оборотом (квітень 2023 — дотепер).</li>
    <li>Управління Unit-економікою напряму та супровід бізнесу на шляху до цільових показників операційної прибутковості та EBITDA підрозділу.</li>
    <li>Формування стратегічного роадмапу платформи та визначення пріоритетів розвитку цифрового продукту в інтересах бізнес-напряму.</li>
    <li>Побудова, розвиток та координація крос-функціональної взаємодії між командами маркетингу, розвитку та відкриття, комерції, напрямку мерчантів, аналітики та операційним департаментом холдингу.</li>
    <li>Впровадження системи регулярних гостьових, продуктових та поведінкових досліджень як інструменту для прийняття стратегічних рішень щодо розвитку комерційних вертикалей.</li>
    <li>Проведення стратегічних івентів з розвитку продукту, участь у стратегічних сесіях напряму та холдингу в цілому.</li>
  </ul>
  <p class="label">Ключові проєкти та результати:</p>
  <ul>
    <li>Керування під ключ та координація запусків масштабних стратегічних партнерств із міжнародними агрегаторами (Glovo, Bolt Food) та великими системними B2B-сервісами (Ліки24 та інші).</li>
    <li>Забезпечення бізнесового та аналітичного супроводу з боку LOKO у проєктах географічної експансії сервісу, що дозволило розгорнути найбільшу Q-commerce мережу в Україні (понад 60 міст та 150+ операційних полігонів, випередивши міжнародних агрегаторів) у синергії з операційною командою холдингу.</li>
    <li>Формування ціннісної архітектури продукту (CVP), оптимізація користувацьких сценаріїв (CJM) та стратегічна валідація Product-Market Fit для масштабування комерційних вертикалей платформи.</li>
    <li>Розробка і впровадження інструментів динамічного управління порогами доставки, моделей Surge Price та механіки двоетапної оплати замовлень, спрямованих на системне покращення Unit-економіки підрозділу.</li>
  </ul>

  <p class="company">VARUS Ecommerce<span class="dates"> | 2020 — 2023</span></p>
  <p class="context">Контекст: VARUS — національна мережа супермаркетів; e-commerce дирекція — виділений бізнес-юніт, що забезпечує повний цикл онлайн-продажів та омніканальної доставки продуктів харчування (E-Grocery).</p>
  <p class="role">Заступник директора з електронної комерції (Deputy Director), Операційний директор (COO)<span class="dates"> | 2020 — 2023</span></p>
  <p class="intro">Стратегічне управління, фінансове планування та повний контроль P&amp;L-показників діджитал-дирекції компанії. Розробка, впровадження та виведення на цільову рентабельність операційної бізнес-моделі онлайн-напряму. Керування крос-функціональними вертикалями: асортиментна політика, ціноутворення, інфраструктура збирання замовлень, внутрішня логістика «останньої милі», digital-маркетинг та єдиний клієнтський сервіс.</p>
  <p class="label">Ключові результати:</p>
  <ul>
    <li>Комплексний аудит операційних процесів та проєктування з нуля верхньорівневої архітектури нової e-commerce платформи компанії, включаючи організацію тендерів та вибір технологічних підрядників.</li>
    <li>Налагодження процесів продуктової розробки з ефективною синхронізацією внутрішніх IT-команд та зовнішніх розробників.</li>
    <li>Проєктування інфраструктурної та фінансової моделі відкриття великого Dark Store, включаючи аудит поточних потужностей, прорахунок Unit-економіки проєкту та формування техніко-економічного обґрунтування для затвердження бюджетування.</li>
    <li>Перебудова логістичної моделі «останньої милі», впровадження нових стандартів контролю часових слотів та збереження температурного режиму доставки.</li>
    <li>Реалізація низки стратегічних та соціальних проєктів, включаючи розгортання благодійної платформи «Кошики Добра».</li>
  </ul>

  <p class="company">Група компаній АЛЛО<span class="dates"> | 2007 — 2020</span></p>
  <p class="context">Контекст: АЛЛО — національний ритейлер та один із найбільших e-commerce маркетплейсів України в сегменті споживчої електроніки та техніки.</p>
  <p class="role">Керівник онлайн-напряму, Керівник відділу розвитку бізнесу АЛЛО-online<span class="dates"> | 2016 — 2020</span></p>
  <p class="intro">Стратегічне управління, бюджетування та операційне планування діяльності онлайн-департаменту компанії. Розробка та реалізація стратегії омніканального бізнесу (Omnichannel) та побудова платформи маркетплейсу. Керування комерційними перемовинами з ключовими українськими та закордонними партнерами.</p>
  <p class="label">Ключові результати:</p>
  <ul>
    <li>Проєктування архітектури та запуск масштабування платформи інтернет-магазину у повноцінний Highload продукт: маркетплейс платформа, адаптивний сайт та мобільний застосунок.</li>
    <li>Впровадження системи наскрізної аналітики та моделей ROPO (Research Online, Purchase Offline), що дозволило точно оцінювати взаємозв'язок діджитал-трафіку з продажами у фізичній роздрібній мережі.</li>
    <li>Формування внутрішньої структури розробки та супроводу цифрових продуктів, налагодження синхронної роботи кількох внутрішніх та зовнішніх команд за методологіями Agile.</li>
    <li>Позиціонування онлайн-підрозділу як внутрішнього центру технологічних інновацій, що прискорило впровадження нових інструментів у масштабах усієї компанії.</li>
  </ul>

  <p class="role">Керівник відділу продажів АЛЛО-online, Директор філії інтернет-магазину<span class="dates"> | 2007 — 2016</span></p>
  <p class="intro">Побудова та масштабування операційної інфраструктури інтернет-магазину від регіонального представництва до загальнонаціонального департаменту продажів. Управління повним циклом замовлення: від моменту генерації ліда до кінцевої доставки споживачеві. Фінансове планування, оптимізація витратної частини та автоматизація бізнес-процесів супроводу продажів.</p>
  <p class="label">Ключові результати:</p>
  <ul>
    <li>Перебудова логістичних процесів взаємодії з національними транспортними операторами та внутрішніми складами, що скоротило терміни доставки замовлень та знизило питомі витрати на логістику.</li>
    <li>Розробка та інтеграція технічних завдань для автоматизації документообігу, обробки замовлень і супроводу клієнтів у внутрішніх ІТ-системах компанії.</li>
    <li>Впровадження KPI-матриці та диференційованої системи фінансової мотивації для лінійного персоналу, що забезпечило зростання ефективності обробки замовлень.</li>
    <li>Організація роботи Дніпропетровської філії з нуля, виведення підрозділу на цільові показники рентабельності, після чого отримав підвищення до керівника національного відділу.</li>
  </ul>

  <p class="company">Приватний підприємець<span class="dates"> | 2006 — 2007</span></p>
  <ul>
    <li>Побудова власної справи у сфері телематики: продаж та впровадження систем GPS-трекінгу та моніторингу автотранспорту для приватних компаній та фізичних осіб.</li>
  </ul>

  <p class="company">ТОВ Плей Мобайл Технолоджі, Менеджер з продажу<span class="dates"> | 2005 — 2007</span></p>
  <ul>
    <li>Розвиток B2B-напряму мобільного зв'язку: прямі продажі, залучення юридичних осіб та організація корпоративних підключень національних операторів.</li>
  </ul>

  <p class="extra-title">Додаткова інформація:</p>
  <p class="extra-title">Стратегічна експертиза та компетенції</p>
  <ul>
    <li><b>Масштаб управління:</b> Досвід керівництва бізнес-юнітами чисельністю 150+ осіб у компаніях із понад 10 000 працівників.</li>
    <li><b>Організаційні зміни:</b> Реструктуризація бізнес-процесів та оптимізація управлінських структур холдингів на основі методології Іцхака Адізеса.</li>
    <li><b>Цифрова трансформація:</b> Глибока експертиза в архітектурі Highload-платформ, Omnichannel-ритейлі та моделюванні складних операційних систем.</li>
    <li><b>Управління досвідом (CX/EX):</b> Розробка наскрізних програм сервісної культури, системне впровадження та масштабування метрик NPS (лояльність клієнтів) та eNPS (залученість команд).</li>
    <li><b>Кризовий та антикризовий менеджмент:</b> Успішне розгортання нових бізнес-вертикалей з нуля та стабілізація операційних процесів в умовах жорстких ринкових обмежень.</li>
    <li><b>Top-level комунікації:</b> Проведення складних комерційних переговорів на міжнародному рівні, публічні виступи та пітчинг проєктів перед інвесторами й акціонерами.</li>
  </ul>

  <p class="extra-title">Сертифікація та мови</p>
  <ul>
    <li><b>Project Management:</b> Сертифікат з управління проєктами U Open University (Lic. UOU2018032503).</li>
    <li><b>Executive тренінги:</b> Лідерські компетенції (А. Станченко), Дизайн корпоративної культури (В. Давтян), Стратегічні бізнес-комунікації.</li>
    <li><b>Англійська</b> — Upper-Intermediate (B2)</li>
  </ul>
</body>
</html>
"""


HTML_EN = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Denis Parshentsev — CV</title>
  <style>
    @font-face {
      font-family: "CV";
      src: url("arial.ttf") format("truetype");
      font-weight: 400;
      font-style: normal;
      font-display: block;
    }
    @font-face {
      font-family: "CV";
      src: url("arialbd.ttf") format("truetype");
      font-weight: 700;
      font-style: normal;
      font-display: block;
    }
    @font-face {
      font-family: "CV";
      src: url("ariali.ttf") format("truetype");
      font-weight: 400;
      font-style: italic;
      font-display: block;
    }
    @font-face {
      font-family: "CV";
      src: url("arialbi.ttf") format("truetype");
      font-weight: 700;
      font-style: italic;
      font-display: block;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    html, body {
      font-family: "CV", Arial, sans-serif;
      font-size: 13pt;
      line-height: 1.32;
      color: #000;
      background: #fff;
      font-synthesis: none;
      -webkit-font-smoothing: antialiased;
      print-color-adjust: exact;
      -webkit-print-color-adjust: exact;
    }

    .photo {
      float: right;
      width: 187pt;
      height: 250pt;
      object-fit: cover;
      object-position: 50% 18%;
      margin: 0 0 12pt 14pt;
    }

    h1 {
      font-size: 30pt;
      font-weight: 700;
      line-height: 1.12;
      margin: 0 0 10pt;
    }

    .meta {
      font-size: 14pt;
      line-height: 1.4;
      margin-bottom: 3pt;
    }

    a { color: #1155CC; text-decoration: underline; }

    h2 {
      font-size: 15pt;
      font-weight: 700;
      margin: 16pt 0 8pt;
      clear: none;
    }

    h2.block { clear: both; padding-top: 4pt; }

    ul { margin: 0 0 6pt 22pt; padding: 0; }
    li { margin: 0 0 3.5pt; }

    .company {
      font-weight: 700;
      font-style: italic;
      margin: 18pt 0 5pt 0;
      padding-left: 22pt;
      position: relative;
    }
    .company::before {
      content: "●";
      position: absolute;
      left: 5pt;
      font-style: normal;
      font-weight: 400;
    }

    .context { font-style: italic; margin: 0 0 7pt 22pt; }
    .role { font-weight: 700; font-style: italic; margin: 14pt 0 5pt 22pt; }
    .role .dates, .company .dates { white-space: nowrap; }
    .context + .role { margin-top: 2pt; }
    ul + .role { margin-top: 20pt; }
    .intro { margin: 0 0 6pt 22pt; }
    .label { font-weight: 700; margin: 11pt 0 5pt 22pt; }
    .extra-title { font-weight: 700; font-size: 14pt; margin: 18pt 0 8pt; }
  </style>
</head>
<body>
  <img class="photo" src="photo.png" alt="Denis Parshentsev">

  <h1>Denis Parshentsev</h1>
  <p class="meta"><b>25 Nov 1981</b></p>
  <p class="meta"><b>City:</b> Dnipro</p>
  <p class="meta"><b>Phone:</b> +380 50 363 31 27</p>
  <p class="meta"><b>Email:</b> <a href="mailto:parshencevdenis@gmail.com">parshencevdenis@gmail.com</a></p>
  <p class="meta"><b>LinkedIn:</b> <a href="https://www.linkedin.com/in/denis-parshentsev/">linkedin.com/in/denis-parshentsev/</a></p>
  <p class="meta"><a href="https://parshentsev-cv.vercel.app/site?lang=en"><b>Web CV</b></a></p>

  <h2>Areas of specialization:</h2>
  <ul>
    <li><b>E-commerce &amp; Q-commerce</b> (managing high-load digital ecosystems).</li>
    <li><b>Retail</b> (transforming traditional retail into omnichannel).</li>
    <li><b>IT / Digital Products</b> (leading product teams and launching systems from scratch).</li>
    <li><b>Logistics &amp; Supply Chain</b> (last-mile, fulfillment and dark store infrastructure).</li>
  </ul>

  <h2>Target positions:</h2>
  <ul>
    <li>Chief Executive Officer (CEO)</li>
    <li>Chief Operating Officer (COO)</li>
    <li>Head of E-commerce / E-commerce Director</li>
    <li>Chief Business Development Officer (CBDO)</li>
  </ul>

  <h2 class="block">Experience:</h2>

  <p class="company">LOKO (Fozzy Group)<span class="dates"> | April 2023 — present</span></p>
  <p class="context">Context: Q-commerce ecosystem within Ukraine's largest grocery retailer.</p>
  <p class="role">Deputy Head of LOKO, Strategic Projects &amp; Partnerships<span class="dates"> | April 2023 — present</span></p>
  <ul>
    <li>Strategic management, financial planning, budgeting and product support while scaling business platform turnover 16× (April 2023 — present).</li>
    <li>Unit economics ownership and support toward target operating profit and division EBITDA.</li>
    <li>Platform strategic roadmap and digital product development priorities for the business line.</li>
    <li>Cross-functional coordination across marketing, expansion, commerce, merchants, analytics and holding operations.</li>
    <li>Guest, product and behavioral research as a basis for strategic decisions on commercial verticals.</li>
    <li>Product development events and participation in division and holding strategy sessions.</li>
  </ul>
  <p class="label">Key projects and results:</p>
  <ul>
    <li>End-to-end management of major partnerships with international aggregators (Glovo, Bolt Food) and large B2B services (Liki24 and others).</li>
    <li>Business and analytics support for geographic expansion — largest Q-commerce network in Ukraine (60+ cities, 150+ operational zones), ahead of international aggregators, in synergy with the holding operations team.</li>
    <li>Product value architecture (CVP), CJM optimization and Product-Market Fit validation for scaling commercial verticals.</li>
    <li>Dynamic delivery thresholds, surge pricing and two-step payment mechanics to improve unit economics.</li>
  </ul>

  <p class="company">VARUS Ecommerce<span class="dates"> | 2020 — 2023</span></p>
  <p class="context">Context: National supermarket chain; dedicated e-commerce unit for full online sales and omnichannel grocery delivery (E-Grocery).</p>
  <p class="role">Deputy Director of E-commerce, Chief Operating Officer (COO)<span class="dates"> | 2020 — 2023</span></p>
  <p class="intro">Strategic management, financial planning and full P&amp;L control of the digital directorate. Development and profitability of the online business model. Cross-functional verticals: assortment, pricing, order picking, last-mile logistics, digital marketing and unified customer service.</p>
  <p class="label">Key results:</p>
  <ul>
    <li>Operational audit and greenfield architecture of a new e-commerce platform, including tenders and vendor selection.</li>
    <li>Product development processes with effective sync of internal IT and external developers.</li>
    <li>Infrastructure and financial model for a large dark store, unit economics and business case for budget approval.</li>
    <li>Last-mile logistics rebuild, time-slot standards and cold-chain delivery controls.</li>
    <li>Strategic and social projects including the «Baskets of Good» charity platform.</li>
  </ul>

  <p class="company">ALLO Group<span class="dates"> | 2007 — 2020</span></p>
  <p class="context">Context: National retailer and one of Ukraine's largest e-commerce marketplaces in consumer electronics.</p>
  <p class="role">Head of Online Business, Head of Business Development (ALLO-online)<span class="dates"> | 2016 — 2020</span></p>
  <p class="intro">Strategic management, budgeting and operations of the online department. Omnichannel strategy and marketplace platform. Commercial negotiations with key domestic and international partners.</p>
  <p class="label">Key results:</p>
  <ul>
    <li>Architecture and scaling of the online store into a high-load marketplace, adaptive website and mobile app.</li>
    <li>End-to-end analytics and ROPO models linking digital traffic to in-store sales.</li>
    <li>In-house digital product structure and Agile sync across internal and external teams.</li>
    <li>Online unit as internal innovation hub accelerating company-wide tool adoption.</li>
  </ul>

  <p class="role">Head of ALLO-online Sales, Internet Store Branch Director<span class="dates"> | 2007 — 2016</span></p>
  <p class="intro">Built and scaled online sales infrastructure from a regional office to a national sales department. Full order cycle from lead to delivery. Financial planning, cost optimization and sales process automation.</p>
  <p class="label">Key results:</p>
  <ul>
    <li>Logistics rebuild with national carriers and warehouses — shorter delivery times and lower unit logistics cost.</li>
    <li>Technical specifications for document flow, order processing and customer support in internal IT systems.</li>
    <li>KPI matrix and differentiated incentive system improving order processing efficiency.</li>
    <li>Built the Dnipro branch from scratch to target profitability, then promoted to head of the national department.</li>
  </ul>

  <p class="company">Private entrepreneur<span class="dates"> | 2006 — 2007</span></p>
  <ul>
    <li>Built a telematics business: sales and implementation of GPS tracking and fleet monitoring for companies and individuals.</li>
  </ul>

  <p class="company">Play Mobile Technology LLC<span class="dates"> | 2005 — 2007</span></p>
  <ul>
    <li>B2B mobile telecom: direct sales, corporate client acquisition and corporate subscriptions with national operators.</li>
  </ul>

  <p class="extra-title">Additional information:</p>
  <p class="extra-title">Strategic expertise and competencies</p>
  <ul>
    <li><b>Leadership scale:</b> Units of 150+ people within companies of 10,000+ employees.</li>
    <li><b>Organizational change:</b> Process restructuring and management optimization using Ichak Adizes methodology.</li>
    <li><b>Digital transformation:</b> High-load platforms, omnichannel retail and complex operating systems.</li>
    <li><b>CX / EX:</b> Service culture programs, NPS and eNPS at scale.</li>
    <li><b>Crisis management:</b> Launching new verticals from scratch and stabilizing operations under tight constraints.</li>
    <li><b>Executive communication:</b> Commercial negotiations, public speaking and investor pitching.</li>
  </ul>

  <p class="extra-title">Certification and languages</p>
  <ul>
    <li><b>Project Management:</b> U Open University certificate (Lic. UOU2018032503).</li>
    <li><b>Executive programs:</b> Leadership Competencies (A. Stanchenko), Corporate Culture Design (V. Davtyan), Strategic Business Communications.</li>
    <li><b>English</b> — Upper-Intermediate (B2)</li>
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
    (BUILD / "cv-uk.html").write_text(HTML, encoding="utf-8")
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
            margin={"top": "14mm", "bottom": "14mm", "left": "14mm", "right": "14mm"},
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
