# ADR-0002: Tailwind Play CDN Tradeoff

## Status

Superseded by [ADR-0005](0005-compiled-tailwind-and-strict-csp-scripts.md)

## Context

The project budget is 24 hours and the current scope is template-only. A compiled frontend pipeline would add setup and build complexity before there is enough surface area to justify it.

## Decision (historical)

Use the Tailwind Play CDN for the MVP. The design tokens are defined in `base.html` and Tailwind is configured inline.

## Consequences (historical)

The CDN required allowing inline scripts in the Content Security Policy. That was a known security tradeoff. The project later moved to compiled CSS per ADR-0005.
