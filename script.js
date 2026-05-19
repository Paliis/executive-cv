(function () {
  const STORAGE_KEY = "cv-lang";
  const { meta, impact, specializations, experience, expertise, roles, industries, certification } =
    window.CV_CONTENT;

  let currentLang = localStorage.getItem(STORAGE_KEY) || "en";

  const header = document.getElementById("header");
  const navToggle = document.getElementById("navToggle");
  const navList = document.getElementById("navList");
  const navBrand = document.getElementById("navBrand");
  const navLinks = document.querySelectorAll(".nav__link");
  const backToTopBtn = document.getElementById("backToTop");
  const langButtons = document.querySelectorAll(".lang-switch__btn");
  const sections = document.querySelectorAll("main section[id]");

  function t(key) {
    const parts = key.split(".");
    let val = window.CV_CONTENT[currentLang];
    for (const p of parts) {
      val = val?.[p];
    }
    return val ?? "";
  }

  function escapeHtml(str) {
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function pill(text) {
    return `<span class="pill">${escapeHtml(text)}</span>`;
  }

  function listItems(items) {
    return `<ul class="exp-card__list">${items.map((i) => `<li>${escapeHtml(i)}</li>`).join("")}</ul>`;
  }

  function renderPills(containerId, items) {
    document.getElementById(containerId).innerHTML = items.map(pill).join("");
  }

  function renderImpact() {
    document.getElementById("impactGrid").innerHTML = impact[currentLang]
      .map(
        (item) => `
      <article class="impact-card card reveal">
        <div class="impact-card__metric">${escapeHtml(item.metric)}</div>
        <p class="impact-card__desc">${escapeHtml(item.desc)}</p>
      </article>`
      )
      .join("");
  }

  function renderSpecializations() {
    document.getElementById("whatGrid").innerHTML = specializations[currentLang]
      .map(
        (item) => `
      <article class="feature-card card reveal">
        <h3>${escapeHtml(item.title)}</h3>
        <p>${escapeHtml(item.desc)}</p>
      </article>`
      )
      .join("");
  }

  function renderExpertise() {
    document.getElementById("expertiseGrid").innerHTML = expertise[currentLang]
      .map(
        (item) => `
      <article class="expertise-card card reveal">
        <h3>${escapeHtml(item.title)}</h3>
        <p>${escapeHtml(item.desc)}</p>
      </article>`
      )
      .join("");
  }

  function renderExperience() {
    document.getElementById("expList").innerHTML = experience[currentLang]
      .map((job) => {
        const resultsLabel = job.resultsKey ? t(job.resultsKey) : t("resultsLabelShort");
        let body = "";
        if (job.intro) {
          body += `<p class="exp-card__intro">${escapeHtml(job.intro)}</p>`;
        }
        if (job.duties?.length) {
          body += listItems(job.duties);
        }
        if (job.results?.length) {
          body += `<p class="exp-card__results-label">${escapeHtml(resultsLabel)}</p>${listItems(job.results)}`;
        }
        const context = job.context
          ? `<p class="exp-card__context">${escapeHtml(job.context)}</p>`
          : "";
        const role = job.role ? `<p class="exp-card__role-sub">${escapeHtml(job.role)}</p>` : "";

        return `
      <li class="timeline__item">
        <article class="exp-card card reveal">
          <div class="exp-card__head">
            <div class="exp-card__head-main">
              <h3 class="exp-card__company">${escapeHtml(job.company)}</h3>
              ${role}
              ${context}
            </div>
            <span class="exp-card__period">${escapeHtml(job.period)}</span>
          </div>
          ${body}
        </article>
      </li>`;
      })
      .join("");
  }

  function renderCertification() {
    const footerCert = document.getElementById("footerCert");
    if (!footerCert) return;

    footerCert.setAttribute("aria-label", t("certSectionLabel"));
    footerCert.innerHTML = certification[currentLang]
      .map(
        (item) => `
      <article class="footer__cert">
        <p class="footer__cert-label">${escapeHtml(item.label)}</p>
        <p class="footer__cert-text">${escapeHtml(item.text)}</p>
        ${item.detail ? `<p class="footer__cert-meta">${escapeHtml(item.detail)}</p>` : ""}
      </article>`
      )
      .join("");
  }

  function setMetaContent(selector, value) {
    const el = document.querySelector(selector);
    if (el && value) el.setAttribute("content", value);
  }

  function updateShareMeta(lang) {
    const title = t("pageTitle");
    const description = t("pageDescription");
    const imageAlt = meta.photoAlt?.[lang] || meta.photoAlt?.en || "";
    const pageUrl = meta.siteUrl + (meta.sharePath || "/");
    const imageUrl = meta.siteUrl + (meta.shareImage || "/photo.png");

    setMetaContent('meta[name="description"]', description);
    setMetaContent('meta[property="og:title"]', title);
    setMetaContent('meta[property="og:description"]', description);
    setMetaContent('meta[property="og:url"]', pageUrl);
    setMetaContent('meta[property="og:image"]', imageUrl);
    setMetaContent('meta[property="og:image:alt"]', imageAlt);
    setMetaContent('meta[property="og:locale"]', lang === "uk" ? "uk_UA" : "en_US");
    setMetaContent('meta[name="twitter:title"]', title);
    setMetaContent('meta[name="twitter:description"]', description);
    setMetaContent('meta[name="twitter:image"]', imageUrl);
    setMetaContent('meta[name="twitter:image:alt"]', imageAlt);
  }

  function applyLanguage(lang) {
    currentLang = lang;
    localStorage.setItem(STORAGE_KEY, lang);
    document.documentElement.lang = lang === "uk" ? "uk" : "en";

    document.title = t("pageTitle");
    updateShareMeta(lang);

    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      const value = t(key);
      if (value) el.textContent = value;
    });

    const nav = document.querySelector(".nav");
    if (nav) nav.setAttribute("aria-label", t("navLabel"));

    const langSwitch = document.getElementById("langSwitch");
    if (langSwitch) langSwitch.setAttribute("aria-label", t("langSwitchLabel"));

    const name = meta.name[lang];
    document.getElementById("navName").textContent = name;
    document.getElementById("footerName").textContent = name;
    const heroName = document.getElementById("heroName");
    if (heroName) heroName.textContent = name;
    document.getElementById("heroLocation").textContent = meta.location[lang];
    const contactLoc = document.getElementById("contactLocation");
    if (contactLoc) contactLoc.textContent = meta.location[lang];
    document.getElementById("contactPhone").textContent = meta.phoneDisplay[lang];
    document.getElementById("contactLinkedin").textContent = meta.linkedinLabel;
    document.querySelector(".nav__brand-icon").textContent = meta.initials;

    const heroPhoto = document.getElementById("heroPhoto");
    if (heroPhoto && meta.photoAlt) heroPhoto.alt = meta.photoAlt[lang];

    if (backToTopBtn) {
      const topLabel = t("backToTopLabel");
      backToTopBtn.setAttribute("aria-label", topLabel);
      backToTopBtn.setAttribute("title", topLabel);
    }

    renderPills("industriesPills", industries[lang]);
    renderPills("rolesPills", roles[lang]);
    renderImpact();
    renderSpecializations();
    renderExpertise();
    renderExperience();
    renderCertification();

    langButtons.forEach((btn) => {
      const active = btn.dataset.lang === lang;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", String(active));
    });

    updateMenuAria();
    initReveal();
    updatePageNav();
  }

  function updateMenuAria() {
    const isOpen = navList.classList.contains("is-open");
    navToggle.setAttribute("aria-label", t(isOpen ? "menuClose" : "menuOpen"));
  }

  function closeMobileNav() {
    navList.classList.remove("is-open");
    navToggle.classList.remove("is-open");
    navToggle.setAttribute("aria-expanded", "false");
    updateMenuAria();
  }

  function updatePageNav() {
    const offset = header.offsetHeight + 80;
    const y = window.scrollY;

    if (backToTopBtn) backToTopBtn.classList.toggle("is-visible", y > 400);

    let currentId = "top";
    if (y + offset >= 80) {
      sections.forEach((section) => {
        if (section.offsetTop <= y + offset) currentId = section.id;
      });
    }

    navLinks.forEach((link) => {
      link.classList.toggle("is-active", link.getAttribute("href") === `#${currentId}`);
    });
  }

  langButtons.forEach((btn) => {
    btn.addEventListener("click", () => applyLanguage(btn.dataset.lang));
  });

  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  window.addEventListener(
    "scroll",
    () => {
      header.classList.toggle("is-scrolled", window.scrollY > 16);
      updatePageNav();
    },
    { passive: true }
  );

  window.addEventListener("resize", updatePageNav, { passive: true });

  navToggle.addEventListener("click", () => {
    const isOpen = navList.classList.toggle("is-open");
    navToggle.classList.toggle("is-open", isOpen);
    navToggle.setAttribute("aria-expanded", String(isOpen));
    updateMenuAria();
  });

  navLinks.forEach((link) => {
    link.addEventListener("click", closeMobileNav);
  });

  if (navBrand) navBrand.addEventListener("click", closeMobileNav);
  if (backToTopBtn) backToTopBtn.addEventListener("click", closeMobileNav);

  updatePageNav();

  let revealObserver;
  function initReveal() {
    if (revealObserver) revealObserver.disconnect();
    revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08 }
    );
    document.querySelectorAll(".reveal").forEach((el) => revealObserver.observe(el));
  }

  document.querySelectorAll(".hero__kicker, .hero__top-text, .hero__profile, .hero__industries, .hero__photo").forEach((el) => {
    if (!el.classList.contains("reveal")) el.classList.add("reveal");
  });

  applyLanguage(currentLang);
})();
