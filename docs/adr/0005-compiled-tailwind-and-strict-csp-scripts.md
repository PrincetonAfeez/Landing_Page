# ADR-0005: Compiled Tailwind CSS and strict CSP for scripts

## Status

Accepted

## Context

ADR-0002 accepted the Tailwind Play CDN so the MVP could ship without a Node build. That required `unsafe-inline` in CSP for the inline Tailwind configuration script, and all utilities were generated at runtime in the browser.

## Decision

Compile Tailwind CSS with the official CLI (`tailwindcss`) into `pages/static/pages/css/site.css`. Templates load that file via `{% static %}`. Theme tokens and base layout styles live in `frontend/src/site.css`. Lucide initialization moves to `pages/static/pages/js/lucide-init.js` (also served via `{% static %}`).

CSP drops `UNSAFE_INLINE` from `script-src` and `style-src`, and removes `https://cdn.tailwindcss.com` from both directives. Scripts are allowed from `self` and `https://unpkg.com` (Lucide UMD only). Stylesheets are allowed from `self` and Google Fonts CSS.

## Consequences

Changing Tailwind classes requires running `npm run build:css` before shipping (or wiring the command into CI before `collectstatic`). The built CSS is committed so clones can run Django without Node until they change styles.

This supersedes the security tradeoff documented in ADR-0002 for inline Tailwind configuration.
