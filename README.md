# CV сайт — Денис Паршенцев

Контент **лише з Google Doc** (експорт у `cv-google.txt` для перевірки), плюс контакти з власника: email `parshencevdenis@gmail.com`.

Google / Bing **навмисно не індексують** (robots.txt + googlebot/bingbot noindex). Візитка для посилання рекрутеру, не для пошуку за ім’ям. Доступ за URL не обмежений.

## Перевірки

```bash
npm test          # контент, i18n, HTML, SEO
npm run test:smoke  # продакшен (parshentsev-cv.vercel.app)
```

## Запуск

Локально: відкрийте `site.html` у браузері (або `index.html` — людину перекине на `/site`).

**Посилання для месенджерів (прев’ю):** https://parshentsev-cv.vercel.app/?v=2  
**Сама візитка:** https://parshentsev-cv.vercel.app/site  
**Українська / англійська:** `?lang=uk` або `?lang=en` (наприклад `/site?lang=uk`). Вибір також пишеться в браузер.

Корінь `/` перенаправляє на `/?v=2` (Telegram кешує кожну URL окремо). Людей з `/` і `/?v=2` JS веде на `/site`, зберігаючи `lang`.

Репозиторій: https://github.com/Paliis/executive-cv — після push у `main` Vercel деплоїть автоматично.

## Аналітика

На `/site` підключено **Vercel Web Analytics** (перегляди сторінок). Увімкніть у кабінеті:

1. [Vercel → parshentsev-cv → Analytics](https://vercel.com/paliis-projects/parshentsev-cv/analytics)
2. **Enable** / **Web Analytics**

Звіти з’являться там після перших візитів (інколи з затримкою кілька хвилин).

PDF: `cv.pdf` (UA) і `cv-en.pdf` (EN) — кнопка Download на сайті дає файл мови інтерфейсу.

```bash
npm run generate:cv      # обидва PDF
npm run generate:photo   # photo.webp / photo.avif
npm test && npm run test:logic
```

## Оновлення з Google Docs

1. Змініть документ у Google.
2. Завантажте експорт:  
   `https://docs.google.com/document/d/1wgNa84lzVahuCf2NnqPb7691gwq7p2lt/export?format=txt`
3. Оновіть `content.js` відповідно до нового тексту (або попросіть асистента синхронізувати).

Документ має бути доступний **для перегляду всіма за посиланням**.

## Файли

| Файл | Призначення |
|------|-------------|
| `content.js` | Усі тексти сайту |
| `site.html` | Повна візитка |
| `index.html` | OG-лендінг для Telegram (`/?v=2`) |
| `cv.pdf` / `cv-en.pdf` | PDF українською / англійською |
| `cv-google.txt` | Останній експорт з Google Doc |

