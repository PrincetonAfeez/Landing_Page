# Architecture Decision Record
## App 41 — Landing Page
**Academic Marketing Group | Document 1 of 5**
**Status: Accepted**

---

## Context

The Academic Marketing group requires a polished, production-aware landing page for Above Board: a reputation and hiring infrastructure concept for hospitality workers and employers. The application is intentionally presentation-only. It needs to communicate the product idea clearly, render a responsive marketing page, expose basic SEO endpoints, and remain simple enough to evaluate as an academic Django project.

The project uses Django for routing, templates, environment-based settings, static asset loading, test support, and production/security configuration. Public copy is stored in Python content constants instead of a database. Tailwind CSS is compiled into a committed static CSS file, and Lucide icons are loaded through a CDN with a small local initializer.

The decision was to build the app as a small but realistic Django marketing site rather than a static HTML page or a full database-backed product application.

---

## Decisions

### Decision 1 — Django over static HTML or Flask

**Chosen:** A Django project with a `core` project package, a `pages` app, Django templates, URL routing, settings modules, static assets, and Django's test client.

**Rejected:** A single static HTML/CSS page or a lightweight Flask app.

**Reason:** The goal was not only to render a landing page, but to practice production-shaped Django architecture: settings separation, environment variables, template inheritance, context processors, URL routing, sitemap support, custom error handlers, and testable views. Static HTML would have been faster, but it would not demonstrate the same backend web application structure. Flask would have been smaller, but Django better supported the academic objective of learning a conventional full-stack Python web framework.

---

### Decision 2 — Python content constants instead of a database or CMS

**Chosen:** All public copy lives in `pages/content.py` as frozen dataclasses, lists, tuples, and dictionaries. Templates render those values.

**Rejected:** Storing landing page copy directly in templates, in a SQLite database, or in a CMS/admin workflow.

**Reason:** The application is presentation-only. A database would add migrations, model design, admin configuration, and persistence concerns before the page has editable content requirements. Hardcoding copy directly inside templates would make the templates harder to scan and harder to migrate later. Frozen dataclasses provide named structure for hero content, features, pricing tiers, navigation items, and footer links while keeping the build within scope.

---

### Decision 3 — Template inheritance and section includes

**Chosen:** `base.html` defines the page shell, `layouts/marketing.html` defines the marketing layout, `pages/home.html` composes page sections, and small includes render reusable UI such as the navbar, footer, CTA button, and feature cards.

**Rejected:** One large monolithic `home.html` template containing the entire page.

**Reason:** A landing page is visually simple but structurally repetitive. Template inheritance keeps global metadata, fonts, CSS, and scripts in one place. Section includes keep hero, features, pricing, and contact isolated. Component includes make CTA buttons and feature cards reusable without introducing a JavaScript framework or component library.

---

### Decision 4 — Compiled Tailwind CSS over runtime Tailwind Play CDN

**Chosen:** Tailwind CSS is compiled with the Tailwind CLI from `frontend/src/site.css` into `pages/static/pages/css/site.css`. The compiled file is committed so the Django app can run without Node unless CSS classes or Tailwind source change.

**Rejected:** Continuing with Tailwind Play CDN and inline browser-side Tailwind configuration.

**Reason:** The original Play CDN approach was useful for rapid prototyping, but it required weaker Content Security Policy rules and generated utilities at runtime in the browser. Compiled CSS improves production discipline: the browser receives static CSS, CSP can be stricter, and deployment can treat CSS like a normal static asset. The cost is that CSS changes require `npm run build:css`.

---

### Decision 5 — Lucide CDN with local initialization script

**Chosen:** Load Lucide from `https://unpkg.com/lucide@0.469.0/dist/umd/lucide.min.js`, then run a local static initializer at `pages/static/pages/js/lucide-init.js`.

**Rejected:** Bundling icons into a local JavaScript build pipeline or replacing icons with inline SVG in every template.

**Reason:** The project already uses Node only for Tailwind compilation, not for a full frontend bundle. Loading Lucide's UMD build keeps icon usage simple: templates only need `data-lucide` attributes. Moving the initialization into a local static file avoids inline JavaScript and supports a stricter CSP. The accepted trade-off is a runtime browser dependency on unpkg for icons.

---

### Decision 6 — Split settings for base, development, and production

**Chosen:** Shared settings live in `core/settings/base.py`, development overrides in `core/settings/dev.py`, and production overrides in `core/settings/prod.py`. Environment values are read through `django-environ`.

**Rejected:** One settings file with manual conditionals for every environment.

**Reason:** The project needs different behavior locally and in production. Development allows all hosts, enables debug mode, allows localhost websocket/connect sources, and uses console logging. Production disables debug mode, requires explicit environment configuration, enables SSL redirect, sets secure cookies, and enforces HSTS. Splitting settings makes those differences explicit and easier to audit.

---

### Decision 7 — Environment-aware logging

**Chosen:** Development uses human-readable console logs. Production uses JSON logs written to both console and a rotating file at `logs/aboveboard.log`.

**Rejected:** Basic Django default logging or print-based debugging.

**Reason:** Local development should be easy to read in the terminal, while production logs should have stable structured fields and bounded disk usage. The rotating file handler provides local persistence, and the JSON formatter prepares logs for external aggregation systems if the app is deployed later.

---

### Decision 8 — Static SEO support through Django routes

**Chosen:** Add `/robots.txt`, `/sitemap.xml`, and `/og/card.png` as first-class routes.

**Rejected:** Ignoring SEO and social preview endpoints because the page is an academic project.

**Reason:** A marketing landing page is incomplete without basic discoverability and social preview behavior. Django makes these endpoints small and testable. `robots.txt` builds an absolute sitemap URL, `sitemap.xml` uses Django's sitemap framework, and the Open Graph card is returned as a cached PNG response.

---

## Consequences

**Positive:**
- The application demonstrates realistic Django structure without becoming a full product system.
- Content dataclasses keep copy organized and templates focused on presentation.
- Template inheritance and includes create clean boundaries between page shell, layout, sections, and components.
- Compiled Tailwind CSS supports stricter CSP and avoids runtime CSS generation.
- Environment-specific settings make local and production behavior easy to reason about.
- Tests cover the home page, robots.txt, sitemap.xml, and Open Graph PNG route.
- Production logging and security settings show awareness beyond a toy landing page.

**Negative / Trade-offs:**
- Using Django for a presentation-only page is heavier than static HTML.
- The app still depends on a third-party CDN for Lucide icons at runtime.
- Any Tailwind class or source CSS change requires rebuilding the compiled CSS before committing.
- Content updates require code changes because there is no database, admin form, or CMS.
- The production static-file story depends on deployment configuration such as `STATIC_ROOT`, `collectstatic`, and the chosen WSGI/ASGI host.

---

## Alternatives Not Explored

- **Full CMS or admin-editable content:** Rejected because the app has no editorial workflow yet. A CMS would be a larger product feature, not a landing page requirement.
- **React, Vue, or another JavaScript framework:** Not needed. The page is mostly static content, and Django templates are sufficient.
- **Self-hosted Lucide bundle:** Deferred. It would remove the CDN dependency but require more frontend build complexity than the current scope justifies.
- **Database-backed waitlist form:** Omitted intentionally. Current CTAs use `mailto:` links, keeping the page presentation-only.

---

*Constitution reference: Article 1 (architectural thinking), Article 3.4 (larger project classification), Article 4 (engineering quality), and Article 6 (behavior verification).*

---


# Technical Design Document
## App 41 — Landing Page
**Academic Marketing Group | Document 2 of 5**

---

## Overview

Landing Page is a Django 5 marketing site for Above Board. It renders a responsive public landing page using Django templates, Python content constants, compiled Tailwind CSS, and Lucide icons. The app is intentionally presentation-only: it has no user accounts, no custom database models, no form submission layer, and no external API calls from the server.

**Project:** `Landing_Page`
**Primary app:** `pages`
**Entry points:** `manage.py`, `core.urls`, `pages.urls`, `pages.views.home`
**Dependencies:** Django, django-csp, django-environ, python-json-logger, Tailwind CLI, Lucide UMD CDN

---

## Data Flow

```
Browser request
     │
     ▼
Django URL resolver
     │
     ├── "/"              → pages.views.home()
     ├── "/robots.txt"    → pages.views.robots_txt()
     ├── "/sitemap.xml"   → django.contrib.sitemaps.views.sitemap()
     └── "/og/card.png"   → pages.views.open_graph_card()
     │
     ▼
home() loads content constants
     │
     ▼
render("pages/home.html", context)
     │
     ▼
pages/home.html
     │
     ├── extends layouts/marketing.html
     │      └── extends base.html
     │
     ├── includes sections/hero.html
     ├── includes sections/features.html
     ├── includes sections/pricing_teaser.html
     └── includes sections/contact.html
     │
     ▼
base.html loads static CSS, fonts, Lucide CDN, local lucide-init.js
     │
     ▼
HTTP response: rendered HTML
```

The server-side path is synchronous. Django resolves a route, calls a view, builds a context from Python constants and global context processors, renders templates, and returns a normal HTTP response.

---

## Module-Level Structure

```text
Landing Page/
  manage.py
  core/
    urls.py
    context_processors.py
    logging_config.py
    settings/
      base.py
      dev.py
      prod.py
  pages/
    apps.py
    content.py
    views.py
    urls.py
    sitemaps.py
    og_image.py
    templatetags/
      nav_tags.py
    templates/
      base.html
      layouts/marketing.html
      pages/home.html
      components/
      sections/
    static/pages/
      css/site.css
      js/lucide-init.js
    tests/
      test_views.py
  frontend/src/site.css
  requirements/
    base.txt
    dev.txt
    prod.txt
  package.json
  tailwind.config.js
  VERSION
```

---

## Module Dependency Graph

```
manage.py
  └── django.core.management.execute_from_command_line

core.settings.dev
  ├── core.settings.base
  └── core.logging_config.build_logging_config

core.settings.prod
  ├── core.settings.base
  └── core.logging_config.build_logging_config

core.settings.base
  ├── environ
  ├── csp.constants
  └── core.logging_config.build_logging_config

core.urls
  ├── django.contrib.sitemaps.views.sitemap
  ├── django.urls.include/path
  ├── pages.views
  └── pages.sitemaps.StaticViewSitemap

core.context_processors
  ├── django.conf.settings
  ├── django.urls.reverse
  ├── pages.apps.get_site_version
  └── pages.content constants

pages.urls
  └── pages.views

pages.views
  ├── django.http.HttpResponse
  ├── django.shortcuts.render
  ├── django.urls.reverse
  ├── pages.content.HERO/FEATURES/PRICING_TIERS
  └── pages.og_image.OG_CARD_PNG

pages.sitemaps
  ├── django.contrib.sitemaps.Sitemap
  └── django.urls.reverse

pages.templatetags.nav_tags
  ├── django.template.Library
  └── django.urls.reverse

templates
  ├── content passed by views
  ├── site globals passed by core.context_processors.site_context
  ├── static assets
  └── nav_tags.active_link
```

---

## Core Data Structures

### `HeroContent`
Frozen dataclass representing the hero section.

```python
@dataclass(frozen=True)
class HeroContent:
    headline: str
    subhead: str
    primary_cta_label: str
    primary_cta_href: str
    secondary_cta_label: str
    secondary_cta_href: str
```

Used by `sections/hero.html`.

---

### `Feature`
Frozen dataclass representing one feature card.

```python
@dataclass(frozen=True)
class Feature:
    icon: str
    title: str
    description: str
```

Used by `sections/features.html` and `components/feature_card.html`. The `icon` field maps to a Lucide icon name rendered through `data-lucide`.

---

### `PricingTier`
Frozen dataclass representing a pricing/access card.

```python
@dataclass(frozen=True)
class PricingTier:
    name: str
    price: str
    audience: str
    highlights: tuple[str, ...]
```

Used by `sections/pricing_teaser.html`.

---

### `NavItem`
Frozen dataclass representing a header navigation item.

```python
@dataclass(frozen=True)
class NavItem:
    label: str
    url_name: str
    fragment: str = ""
```

`url_name` is resolved through Django's URL reversing. `fragment` supports same-page section anchors.

---

### `FooterLink`
Frozen dataclass representing footer links.

```python
@dataclass(frozen=True)
class FooterLink:
    label: str
    href: str
```

Footer links are grouped in the `FOOTER_LINKS` dictionary.

---

### `CONTENT_SECURITY_POLICY`
Nested dictionary consumed by `django-csp`.

Important directives:
- `default-src`: self
- `script-src`: self and `https://unpkg.com`
- `style-src`: self and Google Fonts CSS
- `img-src`: self and data URIs
- `font-src`: self, data URIs, and Google Fonts
- `frame-ancestors`: none

---

### `LOGGING`
Dictionary produced by `build_logging_config(is_prod)`.

Development logging:
- console handler
- human-readable formatter
- `django` at INFO
- `pages` and `core` at DEBUG

Production logging:
- console handler
- rotating file handler at `logs/aboveboard.log`
- JSON formatter
- `django` at WARNING
- `pages` and `core` at INFO

---

## Function and Class Reference

### `manage.main()`
Sets default `DJANGO_SETTINGS_MODULE` to `core.settings.dev` and delegates to Django's command-line executor.

---

### `pages.views.home(request)`
Renders the main landing page.

Context:
```python
{
    "hero": HERO,
    "features": FEATURES,
    "pricing_tiers": PRICING_TIERS,
}
```

Template:
```python
"pages/home.html"
```

---

### `pages.views.open_graph_card(_request)`
Returns `OG_CARD_PNG` as `image/png`.

Response header:
```text
Cache-Control: public, max-age=86400
```

Used by social preview metadata in `base.html`.

---

### `pages.views.robots_txt(request)`
Builds an absolute sitemap URL with `request.build_absolute_uri(reverse("sitemap"))` and returns:

```text
User-agent: *
Allow: /
Sitemap: <absolute sitemap URL>
```

Content type:
```text
text/plain
```

---

### `pages.views.page_not_found(request, exception)`
Renders `404.html` with status code 404.

---

### `pages.views.server_error(request)`
Renders `500.html` with status code 500.

---

### `core.context_processors.site_context(request)`
Adds shared site values to every template context:

```python
{
    "SITE_NAME": SITE_NAME,
    "TAGLINE": TAGLINE,
    "SITE_VERSION": get_site_version(),
    "IS_PROD": settings.IS_PROD,
    "NAV_ITEMS": NAV_ITEMS,
    "FOOTER_LINKS": FOOTER_LINKS,
    "canonical_url": canonical_url,
    "og_image_url": og_image_url,
}
```

`canonical_url` strips query parameters and fragments. `og_image_url` reverses the Open Graph card route and falls back to an empty string if reversal fails.

---

### `pages.apps._read_version()`
Reads the root `VERSION` file and returns the stripped value. If the file is unavailable or empty, it returns `"0.0.0"`.

---

### `pages.apps.get_site_version()`
Returns the module-level `SITE_VERSION` value loaded during `PagesConfig.ready()`.

---

### `PagesConfig.ready()`
Loads the site version once when Django initializes the app.

---

### `pages.sitemaps.StaticViewSitemap`
Django sitemap class for static views.

Properties:
```python
changefreq = "weekly"
priority = 1.0
```

`items()` returns `["pages:home"]`.
`location(item)` returns `reverse(item)`.

---

### `pages.templatetags.nav_tags.active_link(context, url_name)`
Compares the current request path with the reversed URL path. Returns:

```text
text-brand-primary font-semibold
```

when the link is active. Returns an empty string if no request exists, reverse lookup fails, or the link is not active.

---

### `core.logging_config.build_logging_config(is_prod)`
Returns the appropriate logging dictionary for development or production. In production, it ensures the `logs/` directory exists before configuring the rotating file handler.

---

## Template Breakdown

### `base.html`
Owns the HTML shell:
- document type and language
- viewport and metadata
- Open Graph and Twitter card metadata
- canonical URL
- favicon data URI
- Google Fonts preconnect and stylesheet
- compiled Tailwind CSS static link
- Lucide CDN script
- local Lucide initializer script
- overridable `head_extra`, `content`, and `scripts` blocks

---

### `layouts/marketing.html`
Owns the common marketing layout:
- navbar
- `main` page content block
- footer

---

### `pages/home.html`
Owns page composition:
- hero
- features
- pricing teaser
- contact

---

### `components/navbar.html`
Renders the desktop and mobile navigation. Uses `NAV_ITEMS`, Django URL reversing, fragments, and the `active_link` template tag.

---

### `components/footer.html`
Renders footer copy and grouped `FOOTER_LINKS`. Shows `Development build v{{ SITE_VERSION }}` only when `IS_PROD` is false.

---

### `components/cta_button.html`
Renders primary or secondary CTA styles based on the `variant` value.

---

### `components/feature_card.html`
Renders one feature card and maps the content `icon` field to a Lucide icon.

---

### `sections/hero.html`
Renders the hero headline, subhead, CTA buttons, and a static reputation preview card.

---

### `sections/features.html`
Loops over `features` and includes `components/feature_card.html`.

---

### `sections/pricing_teaser.html`
Loops over `pricing_tiers` and displays the beta/pilot access cards.

---

### `sections/contact.html`
Renders the final contact CTA with a `mailto:` link.

---

## State Management

The application has no custom database-backed state.

State sources:
- Environment variables read by `django-environ`
- `.env` file read from the project root
- `VERSION` file read during app startup
- Static files committed to the repository
- Browser-side runtime state only for the mobile `<details>` menu and Lucide icon replacement
- Production log files under `logs/`

SQLite is configured as the default database, but the app does not define custom models. The database exists mostly because Django expects a database setting and tests may touch the database layer.

---

## Error Handling Strategy

- 404 errors use `pages.views.page_not_found`.
- 500 errors use `pages.views.server_error`.
- `active_link()` catches `NoReverseMatch` and returns an empty class string.
- `site_context()` catches `NoReverseMatch` for the Open Graph image route and falls back to an empty image URL.
- `_read_version()` catches `OSError` and falls back to `"0.0.0"`.
- Production logging captures Django/core/pages events in JSON format.
- Django handles uncaught view exceptions according to the active settings module.

---

## External Dependencies

| Dependency | Version Range / Source | Purpose |
|---|---:|---|
| Django | `>=5.2,<6.0` | Web framework, templates, routing, test client, sitemap framework |
| django-csp | `>=4.0,<5.0` | Content Security Policy middleware/settings |
| django-environ | `>=0.11,<1.0` | Environment and `.env` parsing |
| python-json-logger | `>=2.0,<4.0` | Production JSON logging formatter |
| tailwindcss | `^3.4.17` | CSS compilation from `frontend/src/site.css` |
| Lucide | CDN `0.469.0` | Browser-rendered icons through `data-lucide` attributes |

---

## Concurrency Model

The app uses synchronous Django views. There is no async view code, no threads, no queues, and no background workers.

The project exposes both `WSGI_APPLICATION` and `ASGI_APPLICATION`, but the application logic itself is request/response synchronous. Concurrency is delegated to the chosen WSGI or ASGI server in deployment.

---

## Known Limitations

- No database-backed content editing.
- No CMS or Django admin workflow.
- No real waitlist submission form; CTAs use `mailto:`.
- No JavaScript framework or client-side routing.
- Lucide icons depend on the unpkg CDN.
- Tailwind CSS must be rebuilt after class/source changes.
- `STATIC_ROOT` must be configured before production `collectstatic` if required by the host.
- Open Graph image is static, not dynamically generated per page.
- There is no application-level health endpoint beyond ordinary public routes.

---

## Design Patterns Used

- **Django MVT:** URL routes map to views that render templates with context.
- **Settings split:** base/dev/prod modules separate shared, local, and production behavior.
- **Context processor:** global site values are injected into templates without repeating context in every view.
- **Template inheritance:** `base.html` and `layouts/marketing.html` create reusable page structure.
- **Template partials/components:** reusable includes keep UI sections small.
- **Dataclass content model:** frozen dataclasses define structured, immutable public content.
- **Strategy-like logging factory:** `build_logging_config(is_prod)` returns different logging configurations depending on environment.

---

## Verification Summary

The Django test suite verifies:
- home page returns HTTP 200 and contains the site name
- `robots.txt` returns HTTP 200 and includes an absolute sitemap URL
- `sitemap.xml` returns HTTP 200 and includes the root page
- Open Graph card route returns HTTP 200 and begins with the PNG signature

These tests cover the most important public routes and confirm that the presentation app can render and expose its SEO/static endpoints.

---

*Constitution reference: Article 4 (engineering quality), Article 6 (behavior verification), and Article 8 (valid learner work).*

---


# Interface Design Specification
## App 41 — Landing Page
**Academic Marketing Group | Document 3 of 5**

---

## Public Web Interface

The application exposes a small public HTTP interface.

| Method | Path | View / Handler | Success Status | Content Type | Description |
|---|---|---|---:|---|---|
| `GET` | `/` | `pages.views.home` | 200 | `text/html` | Main Above Board landing page |
| `GET` | `/robots.txt` | `pages.views.robots_txt` | 200 | `text/plain` | Search engine crawling instructions and sitemap URL |
| `GET` | `/sitemap.xml` | Django sitemap view | 200 | XML | Sitemap containing the home page |
| `GET` | `/og/card.png` | `pages.views.open_graph_card` | 200 | `image/png` | Static Open Graph preview image |
| `GET` | unknown route | `pages.views.page_not_found` | 404 | `text/html` | Custom not found page |
| server error | n/a | `pages.views.server_error` | 500 | `text/html` | Custom server error page |

---

## Invocation Syntax

### Local development server

```powershell
python manage.py runserver --settings=core.settings.dev
```

Alternative:

```powershell
$env:DJANGO_SETTINGS_MODULE = "core.settings.dev"
python manage.py runserver
```

### Production-style settings

```powershell
$env:DJANGO_SETTINGS_MODULE = "core.settings.prod"
$env:SECRET_KEY = "<strong-secret>"
$env:ALLOWED_HOSTS = "joinaboveboard.com,www.joinaboveboard.com"
python manage.py runserver
```

### CSS build

```powershell
npm run build:css
```

### Test suite

```powershell
python manage.py test --settings=core.settings.dev
```

---

## Management Command Argument Reference

| Name | Type | Required | Default | Accepted Values | Description |
|---|---|---|---|---|---|
| `command` | choice | Yes | — | `runserver`, `test`, `collectstatic`, Django commands | Django management command to execute |
| `--settings` | str | No | `core.settings.dev` from `manage.py` | `core.settings.dev`, `core.settings.prod`, or another settings module | Selects the Django settings module |
| `addrport` | str | No | Django default | e.g. `127.0.0.1:8000`, `0.0.0.0:8000` | Optional runserver bind address and port |
| `--noinput` | bool | No | false | present / absent | Used with commands such as `collectstatic` to suppress prompts |

The application does not define custom management commands. It uses Django's standard command interface.

---

## npm Script Reference

| Script | Command | Required | Description |
|---|---|---|---|
| `build:css` | `tailwindcss -i ./frontend/src/site.css -o ./pages/static/pages/css/site.css --minify` | Required only after CSS/template class changes | Rebuilds the committed static CSS file |

---

## HTTP Input Contract

### `/`

Accepted input:
- HTTP `GET`
- Optional query string is ignored by the view
- No request body required
- No authentication required
- No cookies required

Validation:
- None at the application level

---

### `/robots.txt`

Accepted input:
- HTTP `GET`
- Request host/scheme are used to build the absolute sitemap URL

Validation:
- None at the application level

---

### `/sitemap.xml`

Accepted input:
- HTTP `GET`
- Request host/scheme are used by Django's sitemap framework

Validation:
- None at the application level

---

### `/og/card.png`

Accepted input:
- HTTP `GET`
- No request body required

Validation:
- None at the application level

---

## Output Contract

### Home page `/`

A successful run emits:
- HTML document
- metadata for description, Open Graph, and Twitter cards
- canonical URL when request context is available
- linked compiled CSS at `{% static 'pages/css/site.css' %}`
- Google Fonts stylesheet
- Lucide UMD script from unpkg
- local `pages/js/lucide-init.js`
- marketing content sections:
  - hero
  - features
  - pricing teaser
  - contact
  - navbar
  - footer

The response should contain the site name `Above Board`.

---

### `/robots.txt`

Successful output format:

```text
User-agent: *
Allow: /
Sitemap: <absolute URL to /sitemap.xml>
```

Encoding:
```text
UTF-8 text/plain
```

---

### `/sitemap.xml`

Successful output:
- XML sitemap
- includes the home page URL
- generated by Django's sitemap framework

---

### `/og/card.png`

Successful output:
- PNG bytes
- `Content-Type: image/png`
- starts with PNG signature bytes

Response header:
```text
Cache-Control: public, max-age=86400
```

---

## Exit Code Reference

The project does not define custom process exit codes.

| Exit Code | Condition |
|---:|---|
| 0 | Django management command completed successfully |
| Non-zero | Django, Python, dependency import, settings, test failure, or operating system error |

Common non-zero examples:
- missing Python dependency
- invalid settings module
- missing required production environment variable
- failing tests
- static files command failure
- Tailwind build failure through npm

---

## Error Output Behavior

### Development

Development settings use console logs with a human-readable format:

```text
%(asctime)s %(levelname)s %(name)s %(message)s
```

Django debug mode is enabled. Detailed exception pages may be shown locally.

---

### Production

Production settings disable debug mode and configure JSON logs to:
- console
- `logs/aboveboard.log`

JSON log fields include:
- timestamp
- level
- logger name
- message
- module
- function name
- line number

Custom 404 and 500 templates are rendered for public errors.

---

## Environment Variables

| Variable | Type | Required | Default | Settings Module | Description |
|---|---|---|---|---|---|
| `DJANGO_SETTINGS_MODULE` | str | No locally, yes operationally | `core.settings.dev` via `manage.py` | all | Selects settings module |
| `SECRET_KEY` | str | Required in production | local insecure fallback in base settings | base/prod | Django secret key |
| `ALLOWED_HOSTS` | comma/list string | Required in production | `[]` in base, `["*"]` in dev | base/dev/prod | Hostnames Django will serve |
| `DEBUG` | bool | No | `False` in base, `True` in dev | base/dev | Debug mode toggle |

Environment values may be supplied directly through the shell or through a root `.env` file.

---

## Configuration Files

### `.env`

Location:
```text
project root
```

Loaded by:
```python
environ.Env.read_env(BASE_DIR / ".env")
```

Common keys:
```text
DJANGO_SETTINGS_MODULE=core.settings.dev
SECRET_KEY=<secret>
ALLOWED_HOSTS=localhost,127.0.0.1
DEBUG=True
```

Precedence:
- Environment variables already present in the process are respected by Django/environ behavior.
- `.env` provides local defaults when present.

---

### `requirements/base.txt`

Declares runtime Python dependencies:
```text
Django>=5.2,<6.0
django-csp>=4.0,<5.0
django-environ>=0.11,<1.0
python-json-logger>=2.0,<4.0
```

---

### `requirements/dev.txt`

Includes:
```text
-r base.txt
```

No extra dev-only Python packages are currently declared.

---

### `requirements/prod.txt`

Includes:
```text
-r base.txt
```

No extra production-only Python packages are currently declared.

---

### `package.json`

Declares:
- private package
- `build:css` script
- Tailwind CSS dev dependency

---

### `tailwind.config.js`

Defines:
- template scan paths:
  - `./pages/templates/**/*.html`
  - `./pages/templatetags/**/*.py`
- brand color tokens mapped to CSS variables
- `shadow-soft`
- no plugins

---

### `frontend/src/site.css`

Defines:
- Tailwind base/components/utilities imports
- brand CSS variables
- body background/font styles
- `.hero-field` background grid

---

### `VERSION`

Read at Django app startup by `PagesConfig.ready()`. Displayed in the footer only in non-production builds.

---

## Side Effects

| Operation | Side Effect |
|---|---|
| `python manage.py runserver` | Starts a local development server |
| `python manage.py test` | May create or touch local SQLite/test database state |
| `npm run build:css` | Rewrites `pages/static/pages/css/site.css` |
| Production logging | Creates `logs/` and writes `logs/aboveboard.log` |
| Browser loads page | Requests Google Fonts CSS/fonts and Lucide UMD script |
| `collectstatic` | Copies static files to configured `STATIC_ROOT` if configured |

The server-side app does not call external APIs, submit forms, send email, or modify custom application data.

---

## Usage Examples

### Basic local use

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements\dev.txt
Copy-Item .env.example .env
npm install
npm run build:css
python manage.py runserver --settings=core.settings.dev
```

Visit:

```text
http://127.0.0.1:8000/
```

---

### Advanced use — production settings smoke run

```powershell
$env:DJANGO_SETTINGS_MODULE = "core.settings.prod"
$env:SECRET_KEY = "replace-with-real-secret"
$env:ALLOWED_HOSTS = "localhost,127.0.0.1"
python manage.py check --deploy
```

---

### Edge case — verify SEO endpoints

```powershell
python manage.py test --settings=core.settings.dev
```

Or manually open:

```text
http://127.0.0.1:8000/robots.txt
http://127.0.0.1:8000/sitemap.xml
http://127.0.0.1:8000/og/card.png
```

---

### CSS update flow

```powershell
# edit templates or frontend/src/site.css
npm run build:css
python manage.py runserver --settings=core.settings.dev
```

Commit both the source CSS/template change and the rebuilt `pages/static/pages/css/site.css`.

---

### Intentional failure — missing dependency

```powershell
python manage.py runserver --settings=core.settings.dev
```

If dependencies were not installed, expected failure:
```text
ModuleNotFoundError: No module named 'django'
```

Resolution:
```powershell
python -m pip install -r requirements\dev.txt
```

---

### Intentional failure — missing production config

```powershell
$env:DJANGO_SETTINGS_MODULE = "core.settings.prod"
python manage.py check
```

If `SECRET_KEY` or `ALLOWED_HOSTS` is missing in a real production environment, configuration validation or runtime startup should fail or behave incorrectly. Set both variables explicitly before deployment.

---

## Exported Internal Interfaces

The app is not designed as a reusable Python library, but these functions/classes form internal contracts:

- `pages.views.home`
- `pages.views.robots_txt`
- `pages.views.open_graph_card`
- `pages.sitemaps.StaticViewSitemap`
- `pages.templatetags.nav_tags.active_link`
- `core.context_processors.site_context`
- `core.logging_config.build_logging_config`
- `pages.apps.get_site_version`

---

*Constitution reference: Article 6 (verification), Article 4 (input/output boundaries), and Article 8 (understandable and verifiable work).*

---


# Runbook
## App 41 — Landing Page
**Academic Marketing Group | Document 4 of 5**

---

## Requirements

- Python 3.12 target runtime
- Django 5
- Node.js and npm only when installing npm dependencies or rebuilding Tailwind CSS
- Python dependencies from `requirements/dev.txt` or `requirements/prod.txt`
- Tailwind CSS CLI through npm
- Browser access to Google Fonts and unpkg for the full visual/icon experience
- PowerShell commands are shown because the project README uses PowerShell examples

---

## Installation

### Local development setup

```powershell
git clone https://github.com/PrincetonAfeez/Landing_Page.git
cd Landing_Page

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install -r requirements\dev.txt
Copy-Item .env.example .env

npm install
npm run build:css
```

No database migration step is required for custom app models because the application does not define custom models.

---

## Configuration

### Development

Use development settings:

```powershell
$env:DJANGO_SETTINGS_MODULE = "core.settings.dev"
```

Or pass the settings module directly:

```powershell
python manage.py runserver --settings=core.settings.dev
```

Development behavior:
- `DEBUG = True`
- `ALLOWED_HOSTS = ["*"]`
- console logging
- localhost websocket/connect sources allowed in CSP
- footer shows development build version

---

### Production

Set required production variables:

```powershell
$env:DJANGO_SETTINGS_MODULE = "core.settings.prod"
$env:SECRET_KEY = "<strong-secret>"
$env:ALLOWED_HOSTS = "joinaboveboard.com,www.joinaboveboard.com"
```

Production behavior:
- `DEBUG = False`
- explicit `SECRET_KEY`
- explicit `ALLOWED_HOSTS`
- HSTS enabled
- SSL redirect enabled
- secure CSRF/session cookies
- JSON logs to console and rotating file
- stricter CSP
- footer does not show development build version

---

## Running the App

### Development server

```powershell
python manage.py runserver --settings=core.settings.dev
```

Open:

```text
http://127.0.0.1:8000/
```

Expected result:
- HTTP 200
- Above Board landing page renders
- navbar, hero, features, pricing, contact, and footer are visible
- icons render after Lucide loads
- compiled Tailwind styling is applied

---

### Production dependency install

```powershell
python -m pip install -r requirements\prod.txt
npm ci
npm run build:css
```

If the host requires static collection:

```powershell
python manage.py collectstatic --noinput --settings=core.settings.prod
```

Before running `collectstatic`, configure `STATIC_ROOT` in production settings or in host-specific settings.

---

## Running Tests

```powershell
python manage.py test --settings=core.settings.dev
```

Expected result:
- all tests pass
- home page returns 200
- robots.txt returns 200 and includes an absolute sitemap URL
- sitemap.xml returns 200 and includes the root page
- Open Graph card route returns 200 and PNG bytes

---

## Rebuilding CSS

Run this after changing:
- Tailwind classes in templates
- `frontend/src/site.css`
- `tailwind.config.js`

```powershell
npm run build:css
```

Expected result:
```text
pages/static/pages/css/site.css
```

is rewritten with minified compiled CSS.

Commit the rebuilt CSS file with the template/source CSS change.

---

## Standard Operating Procedures

### View the landing page locally

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py runserver --settings=core.settings.dev
```

Visit:

```text
http://127.0.0.1:8000/
```

---

### Verify SEO endpoints

```powershell
python manage.py runserver --settings=core.settings.dev
```

Open:

```text
http://127.0.0.1:8000/robots.txt
http://127.0.0.1:8000/sitemap.xml
http://127.0.0.1:8000/og/card.png
```

Expected:
- `robots.txt` includes `User-agent: *`, `Allow: /`, and `Sitemap:`
- `sitemap.xml` includes the site root URL
- `og/card.png` displays or downloads as a PNG image

---

### Update page copy

1. Edit `pages/content.py`
2. If no Tailwind class changed, CSS rebuild is not required
3. Run tests

```powershell
python manage.py test --settings=core.settings.dev
```

4. Run the server and visually inspect the page

```powershell
python manage.py runserver --settings=core.settings.dev
```

---

### Update page structure

1. Edit the relevant template under `pages/templates/`
2. If Tailwind classes were added or changed, run:

```powershell
npm run build:css
```

3. Run tests:

```powershell
python manage.py test --settings=core.settings.dev
```

4. Visually inspect responsive layout in the browser

---

### Update brand colors or base styling

1. Edit `frontend/src/site.css`
2. Run:

```powershell
npm run build:css
```

3. Run:

```powershell
python manage.py test --settings=core.settings.dev
```

4. Inspect `/` in the browser

---

### Update production logging behavior

1. Edit `core/logging_config.py`
2. Run tests
3. Run with production settings in a safe environment
4. Confirm `logs/aboveboard.log` is created and receives JSON records

---

## Health Checks

### Application health

```text
GET /
```

Healthy:
- Status 200
- Body contains `Above Board`

---

### SEO health

```text
GET /robots.txt
GET /sitemap.xml
```

Healthy:
- `robots.txt` contains an absolute sitemap URL
- `sitemap.xml` contains the root URL

---

### Social preview health

```text
GET /og/card.png
```

Healthy:
- Status 200
- Content-Type includes `image/png`
- Response begins with PNG signature bytes

---

### Static asset health

In the browser developer tools, verify:
- `pages/css/site.css` loads successfully
- `pages/js/lucide-init.js` loads successfully
- Lucide UMD script from unpkg loads successfully
- Google Fonts stylesheet loads successfully

---

## Expected Output Samples

### `robots.txt`

```text
User-agent: *
Allow: /
Sitemap: http://127.0.0.1:8000/sitemap.xml
```

Host may differ depending on the request.

---

### Successful test run

```text
Ran 4 tests
OK
```

Exact timing and database setup messages may vary.

---

### Open Graph image response

Headers should include:

```text
Content-Type: image/png
Cache-Control: public, max-age=86400
```

Body should begin with:

```text
\x89PNG\r\n\x1a\n
```

---

## Known Failure Modes

### `ModuleNotFoundError: No module named 'django'`

**Trigger:** Python dependencies were not installed in the active environment.

**Fix:**
```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements\dev.txt
```

---

### Page renders without styling

**Trigger:** Compiled CSS missing, stale, or not served.

**Diagnostic:**
- Check browser Network tab for `pages/css/site.css`
- Confirm file exists at `pages/static/pages/css/site.css`

**Fix:**
```powershell
npm install
npm run build:css
```

---

### Icons do not render

**Trigger:** Lucide CDN blocked, CSP mismatch, or `lucide-init.js` failed to load.

**Diagnostic:**
- Check browser console for `lucide` errors
- Check Network tab for unpkg and `lucide-init.js`

**Fix:**
- Confirm CSP allows `https://unpkg.com` under `script-src`
- Confirm `pages/static/pages/js/lucide-init.js` is served
- Consider self-hosting Lucide if CDN access is unreliable

---

### Production startup behaves incorrectly

**Trigger:** `SECRET_KEY`, `ALLOWED_HOSTS`, or `DJANGO_SETTINGS_MODULE` missing or wrong.

**Diagnostic:**
```powershell
python manage.py check --settings=core.settings.prod
```

**Fix:**
Set required environment variables explicitly.

---

### `collectstatic` fails or static files are missing in deployment

**Trigger:** `STATIC_ROOT` not configured for the deployment environment, or static files not collected/served.

**Diagnostic:**
- Check production settings
- Check host documentation
- Check whether `pages/static/pages/css/site.css` exists before collection

**Fix:**
- Configure `STATIC_ROOT`
- Run:
```powershell
python manage.py collectstatic --noinput --settings=core.settings.prod
```

---

### Production logs are not written

**Trigger:** App cannot create or write to `logs/aboveboard.log`.

**Diagnostic:**
- Check filesystem permissions
- Check whether `logs/` exists
- Check process user write access

**Fix:**
- Create writable log directory
- Adjust deployment permissions
- Prefer platform stdout logging if file writes are restricted

---

### Footer version shows `0.0.0`

**Trigger:** `VERSION` file missing, unreadable, or empty.

**Diagnostic:**
```powershell
Get-Content VERSION
```

**Fix:**
Write the intended version string to `VERSION`.

---

## Troubleshooting Decision Tree

```text
App will not start
  ├── Missing dependency?
  │     └── Install requirements/dev.txt or requirements/prod.txt
  ├── Wrong settings module?
  │     └── Use --settings=core.settings.dev locally
  └── Production env missing?
        └── Set SECRET_KEY and ALLOWED_HOSTS

Page loads but looks wrong
  ├── CSS missing?
  │     └── Run npm run build:css and check static path
  ├── Fonts blocked?
  │     └── Check Google Fonts network requests and CSP
  └── Icons missing?
        └── Check Lucide CDN and lucide-init.js

SEO endpoints fail
  ├── /robots.txt missing?
  │     └── Check core.urls path and pages.views.robots_txt
  ├── /sitemap.xml missing?
  │     └── Check django.contrib.sitemaps and StaticViewSitemap
  └── /og/card.png broken?
        └── Check pages.og_image.OG_CARD_PNG import

Tests fail
  ├── URL reverse error?
  │     └── Check app_name, route names, and core.urls include
  ├── Response content changed?
  │     └── Update tests only if the behavior intentionally changed
  └── PNG assertion failed?
        └── Confirm OG_CARD_PNG is valid PNG bytes
```

---

## Dependency Failure Handling

### Python dependency failure

Install from the appropriate requirements file:

```powershell
python -m pip install -r requirements\dev.txt
```

or:

```powershell
python -m pip install -r requirements\prod.txt
```

---

### npm/Tailwind failure

Reinstall npm dependencies:

```powershell
Remove-Item -Recurse -Force node_modules
npm install
npm run build:css
```

If using production CI:

```powershell
npm ci
npm run build:css
```

---

### CDN failure

If Google Fonts or Lucide are unavailable:
- The page should still return HTML.
- Fonts may fall back to system UI fonts.
- Icons may not render.

Long-term fix:
- Self-host fonts and Lucide assets.
- Remove CDN allowances from CSP after self-hosting.

---

## Recovery Procedures

### Recover from stale CSS

```powershell
npm run build:css
python manage.py test --settings=core.settings.dev
```

Then visually inspect the page.

---

### Recover from broken `.env`

1. Compare with `.env.example`
2. Restore required keys
3. Restart the Django process

---

### Recover from broken production logs

```powershell
New-Item -ItemType Directory -Force logs
```

Confirm the app process can write to the directory.

---

### Recover from template error

1. Reproduce locally with `core.settings.dev`
2. Read the Django debug page
3. Check the template include path
4. Check context keys from `home()` and `site_context()`
5. Run the test suite after fixing

---

## Logging Reference

### Development

Destination:
```text
stdout/stderr console
```

Format:
```text
timestamp level logger message
```

Logger levels:
- `django`: INFO
- `pages`: DEBUG
- `core`: DEBUG

---

### Production

Destinations:
```text
console
logs/aboveboard.log
```

Format:
```text
JSON
```

Rotation:
```text
maxBytes = 10485760
backupCount = 5
```

Logger levels:
- `django`: WARNING
- `pages`: INFO
- `core`: INFO

---

## Maintenance Notes

- Rebuild Tailwind CSS after changing templates or CSS source.
- Keep CSP aligned with actual script/style/font/image sources.
- Consider self-hosting Lucide and fonts if the page becomes production-critical.
- Add a real waitlist form only when persistence, spam prevention, validation, and privacy requirements are defined.
- Add CI to run Django tests and CSS build before deployment.
- Keep `VERSION` updated if it is used as a visible development build marker.
- Review Django, django-csp, django-environ, and python-json-logger version ranges periodically.

---

*Constitution reference: Article 6 (behavior verification), Article 5 (constraints and trade-offs), and Article 8 (verifiable learner work).*

---


# Lessons Learned
## App 41 — Landing Page
**Academic Marketing Group | Document 5 of 5**

---

## Why This Design Was Chosen

This design was chosen to practice a realistic Django marketing-site architecture without pretending the project was a full product. The application needed to look and behave like a credible landing page while still remaining scoped to presentation, routing, templates, static assets, environment settings, logging, and basic SEO endpoints.

Django was the right learning tool because it forced clean separation between project configuration, URL routing, views, templates, context processors, static files, and tests. A static HTML page would have been faster, but it would not have created the same opportunity to practice production-shaped Python web structure.

The content model was the most important simplifying decision. By keeping public copy in frozen dataclasses inside `pages/content.py`, the project avoided unnecessary database complexity while still giving templates structured data. That made the page easier to update, test, and eventually migrate if the product later needs a database, CMS, or admin workflow.

---

## What Was Intentionally Omitted

**Database-backed content:** The app does not define custom models. This was intentional because the landing page does not yet need persistence. Adding models just to store static marketing copy would create unnecessary migration and admin complexity.

**Waitlist form handling:** The CTAs use `mailto:` links instead of accepting form submissions. A real waitlist would require validation, persistence, spam protection, privacy decisions, confirmation behavior, and operational monitoring. That is a separate product feature, not a requirement for this presentation-focused build.

**JavaScript framework:** No React, Vue, Alpine, or similar framework was added. The page does not need client-side routing or complex browser state. Django templates and small static JavaScript for Lucide initialization are enough.

**Dynamic Open Graph image generation:** The app returns a static PNG for social preview. Dynamic image generation would be interesting, but it would add image rendering logic and more failure modes without improving the core learning objective.

**Self-hosted icon package:** Lucide is loaded from unpkg. Self-hosting would be more production-independent, but it would require extra asset management that is not yet justified by the scope.

**CMS/admin workflow:** A CMS would make sense if non-developers needed to edit copy. For this project, code-level content updates are acceptable and easier to evaluate.

---

## Biggest Weakness

The biggest weakness is the remaining CDN dependency for Lucide icons. The project made a strong move away from runtime Tailwind CDN usage by compiling CSS and tightening CSP, but it still allows `https://unpkg.com` under `script-src` for Lucide.

That is a reasonable academic trade-off, but it leaves the page dependent on a third-party network request for icons. If unpkg is blocked or unavailable, the page still works as HTML, but visual polish degrades. A production-critical version should self-host Lucide assets or replace the icon system with inline SVG components rendered by Django templates.

The second weakness is that the content is code-editable only. That keeps the project clean, but any copy update requires a code change and redeploy. For a real marketing team, that would eventually become friction.

---

## Scaling Considerations

**If traffic increases:**
- Serve static files through a CDN or the hosting platform's static asset layer.
- Ensure `collectstatic` is configured with a proper `STATIC_ROOT`.
- Prefer platform stdout logging over local rotating files if the app runs in containers.
- Add caching headers for static assets and review cache behavior for `/og/card.png`.

**If the marketing site grows to multiple pages:**
- Expand `pages.content` carefully or split content by page.
- Add more sitemap entries.
- Move repeated SEO metadata into a more formal page metadata structure.
- Add tests for every public route.

**If non-developers need content control:**
- Migrate content dataclasses to Django models, a headless CMS, or flat-file content.
- Keep the template contract similar so the migration does not require rewriting all templates.
- Add preview workflows before production publishing.

**If the project becomes a real product front door:**
- Replace `mailto:` CTAs with real form handling.
- Add validation, persistence, spam prevention, and privacy copy.
- Add analytics only after deciding what data collection is appropriate.
- Self-host fonts and icons to reduce external dependencies.

---

## What the Next Refactor Would Be

1. **Self-host Lucide icons** — remove the unpkg runtime dependency and tighten CSP further.

2. **Add a real health endpoint** — expose a simple route that deployment infrastructure can check without parsing the marketing page.

3. **Add CI checks** — run Django tests and `npm run build:css` automatically before deployment or merge.

4. **Formalize page metadata** — move titles, descriptions, canonical behavior, and Open Graph values into a small page metadata object instead of spreading them across template blocks.

5. **Add deployment-specific static settings** — define `STATIC_ROOT` and document the exact production static-file pipeline for the chosen host.

---

## What This Project Taught

- **Django is useful even for simple pages when the learning goal includes architecture.** The project could have been static HTML, but Django created meaningful practice with routing, settings, templates, context processors, tests, and deployment concerns.

- **Content structure matters before a database is needed.** Frozen dataclasses provided a clean middle ground between hardcoded template text and overbuilt persistence.

- **Security trade-offs become visible quickly in frontend tooling.** Tailwind Play CDN made the first version easier, but it weakened CSP. Moving to compiled CSS showed why production frontend assets should be built ahead of time.

- **Template decomposition is architecture, not decoration.** Splitting the page into base, layout, sections, and components made the HTML easier to reason about and reduced the risk of one unreadable monolithic template.

- **Tests can verify marketing-site behavior without being complicated.** The tests do not need to inspect every visual detail. They verify that the public routes respond, important content appears, and SEO/static endpoints behave correctly.

- **Operational details belong in small projects too.** Logging, settings separation, CSP, robots.txt, sitemap.xml, Open Graph metadata, and production flags are not enterprise-only concerns. They are part of building a web app that can be understood and operated.

---

*Constitution v2.0 checklist: This document satisfies Article 5 (trade-off documentation) and Article 7 (progressive complexity) for App 41.*
