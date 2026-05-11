# Landing Page

Academic marketing landing page for Above Board.

This implementation is intentionally presentation-only: Django templates, Python content constants, compiled Tailwind CSS, and Lucide icons (CDN).

## Stack

- Python 3.12 target runtime
- Django 5
- Tailwind CSS (CLI build to static assets; see `package.json` and `frontend/src/site.css`)
- Lucide icons (CDN)
- django-environ
- django-csp
- python-json-logger

**Node.js** is only required to install npm dependencies and run `npm run build:css` when you change styles or templates that use new Tailwind classes. The built file under `pages/static/pages/css/` is committed so you can run the app without Node if you are not editing CSS.

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements\dev.txt
Copy-Item .env.example .env
npm install
npm run build:css
$env:DJANGO_SETTINGS_MODULE = "core.settings.dev"
python manage.py runserver
```

Or in one line for the server:

```powershell
python manage.py runserver --settings=core.settings.dev
```

After changing Tailwind classes or `frontend/src/site.css`, run `npm run build:css` again before committing.

**Tests:**

```powershell
python manage.py test --settings=core.settings.dev
```

`core.settings.dev` enables debug mode, allows all hosts, and uses console logging. A local SQLite file (`db.sqlite3`, gitignored) is created automatically if anything touches the database layer (for example running tests).

## Production setup

Set these environment variables:

```text
DJANGO_SETTINGS_MODULE=core.settings.prod
SECRET_KEY=<strong-secret>
ALLOWED_HOSTS=joinaboveboard.com,www.joinaboveboard.com
```

Install dependencies, rebuild CSS whenever templates or Tailwind sources change, then deploy with your ASGI or WSGI server. If your host uses `collectstatic`, set `STATIC_ROOT` in settings first, then run `python manage.py collectstatic --noinput`.

```powershell
python -m pip install -r requirements\prod.txt
npm ci
npm run build:css
```

Production settings enforce HSTS, SSL redirect, strict referrer policy, frame denial, JSON logs, and the configured CSP.

## Project structure

```text
Landing Page/
  core/                 Django project package: settings, URLs, logging, context processors
  pages/                Landing app: views, content constants, templates, static assets, tests
  frontend/src/         Tailwind entry (`site.css`) compiled into `pages/static/pages/css/`
  docs/adr/             Architecture decision records (ADRs)
  requirements/         base, dev, and prod dependency files
  package.json          npm scripts (`build:css`)
  VERSION               Shown in the footer on non-production builds
```

## Content model

All public copy lives in `pages/content.py` as dataclasses and constants. Templates render those values and use small includes for repeated UI. There is no database, no forms layer, and no JavaScript framework.

## Decisions

See `docs/adr/` for architecture decisions:

- ADR-0001: Content as Python constants
- ADR-0002: Tailwind Play CDN tradeoff (superseded)
- ADR-0003: Logging strategy
- ADR-0004: Site version source
- ADR-0005: Compiled Tailwind CSS and strict CSP for scripts
