# Nayi Raah — Website

A lightweight, SEO-friendly Django site for Nayi Raah ("Nova Vita, Nova Via" —
turning ideas into skills, support into action). Pure Django templates, hand-written
CSS (no Bootstrap/Tailwind/etc.), and only the vanilla JS needed for the mobile
nav toggle.

## Project structure

```
nayiraah/
├── manage.py
├── requirements.txt
├── .env.example              # copy to .env and fill in real values
├── nayiraah_project/         # project-level settings, URLs, WSGI/ASGI
│   ├── settings.py
│   └── urls.py                # includes sitemap.xml + robots.txt
├── core/                      # the one app powering the whole site
│   ├── models.py               # Resource, WorkEntry, SunshineEntry, ContactMessage
│   ├── views.py
│   ├── urls.py
│   ├── forms.py                # ContactForm (with honeypot spam field)
│   ├── admin.py                 # content editing lives in /admin/
│   ├── sitemaps.py
│   └── fixtures/initial_data.json   # starter content (matches the original site)
├── templates/core/            # base.html + one template per page
└── static/
    ├── css/style.css           # entire design system, hand-written
    ├── js/main.js               # nav toggle only
    └── images/
```

## Pages

| URL | Purpose |
|---|---|
| `/` | Home — mission teaser, resource cards, latest work |
| `/about/` | About Nayi Raah |
| `/resources/` | "Find a Path" resources, grouped by category |
| `/work/` | Work Done Till Date — timeline of sessions/activities |
| `/work/<slug>/` | Full write-up of a single session |
| `/sunshine/` | Today's Sunshine — daily quote, meaning, reminder, affirmation |
| `/contact/` | Contact form (replaces the old Google Form embed) |
| `/sitemap.xml` | Auto-generated sitemap |
| `/robots.txt` | Auto-generated, points to the sitemap |
| `/admin/` | Django admin — where you add/edit all content |

## Setup

1. **Create a virtual environment and install dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and fill in a real `DJANGO_SECRET_KEY` (see the comment in the
   file for how to generate one). For local development the defaults
   (`DJANGO_DEBUG=true`) work out of the box.

   Since Django doesn't read `.env` files natively, either:
   - export the variables yourself (`export $(cat .env | xargs)` on macOS/Linux), or
   - install `python-dotenv` and add `load_dotenv()` to the top of `manage.py`, or
   - set them directly in your hosting platform's environment settings (Render, Railway, etc.)

3. **Run migrations and load starter content**
   ```bash
   python manage.py migrate
   python manage.py loaddata initial_data
   ```
   This loads the four resource cards (Education/Wellness/Support/Volunteer),
   today's sunshine quote, and your menstrual hygiene session as the first
   "Work" entry — all editable afterwards in the admin.

4. **Create an admin account**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` for the site and `/admin/` to manage content.

## Adding content

Everything editorial lives in the Django admin (`/admin/`) — no code changes needed:

- **Work Done Till Date** → add a "Work entry": title, date, location, summary,
  full write-up, optional cover photo, optional per-entry SEO overrides.
- **Today's Sunshine** → add a "Sunshine entry" dated for the day you want it
  to appear. If no entry matches today's date, the page falls back to the most
  recent published one, so it's never empty.
- **Find a Path / Resources** → add or edit "Resources", grouped by category
  (Education/Wellness/Support/Volunteer).
- **Contact messages** → every submission through `/contact/` is saved under
  "Contact messages" in the admin, and (if email is configured) emailed to
  the addresses in `DJANGO_ADMINS`.

## SEO

- Every page renders dynamic `<title>`, meta description, Open Graph, Twitter
  Card and canonical tags from `templates/core/base.html`'s reusable `{% block seo %}`.
  Individual views/models can override `meta_title` / `meta_description` /
  `meta_keywords` (see `WorkEntry`'s admin "SEO" fieldset for an example).
- JSON-LD structured data: `NGO` schema site-wide, `Article` schema on each
  work entry detail page.
- `/sitemap.xml` and `/robots.txt` are generated automatically — no static
  files to keep in sync. Update `SITE_DOMAIN` in `.env` once you have a real
  domain so canonical/OG URLs and the sitemap point to the right place.
- Replace `static/images/og-default.jpg` with a real 1200×630 share image
  once you have branded photography.

## Performance notes

- No CSS/JS framework — `static/css/style.css` is the entire stylesheet,
  hand-written and small.
- WhiteNoise serves static files with compression and far-future cache
  headers in production, without needing a separate nginx/CDN layer for a
  site this size. Run `python manage.py collectstatic` before deploying.
- Images use `loading="lazy"` and explicit `width`/`height` to avoid layout shift.
- SQLite is the default database — perfectly adequate at this scale. Swap the
  `DATABASES` block in `settings.py` for Postgres only if you outgrow it.

## Deploying to production

1. Set `DJANGO_DEBUG=false` and a real `DJANGO_SECRET_KEY`.
2. Set `DJANGO_ALLOWED_HOSTS`, `DJANGO_SITE_DOMAIN`, and `DJANGO_CSRF_TRUSTED_ORIGINS`.
3. Run `python manage.py collectstatic --noinput`.
4. Serve with a real WSGI server, e.g.:
   ```bash
   gunicorn nayiraah_project.wsgi:application
   ```
5. Point your domain's DNS at your host, and make sure HTTPS is terminated
   somewhere in front of the app (the security settings assume it is).

## What changed from the original single-page HTML

- Removed the embedded Google Form; replaced with a real server-side contact
  form (CSRF-protected, spam-filtered, saved to the database).
- Split the single-page anchor-link layout into real, separately-routable
  pages (`/about/`, `/resources/`, `/work/`, `/sunshine/`, `/contact/`) with
  their own SEO metadata.
- Added the new "Work Done Till Date" section as a proper timeline, backed by
  a model so new sessions can be added through the admin instead of editing HTML.
- Rebuilt the CSS from scratch as a small, intentional design system (see
  `static/css/style.css`) rather than the ad hoc rules in the original file,
  while keeping the sunflower/path visual identity from your logo.
