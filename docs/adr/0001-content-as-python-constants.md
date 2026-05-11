# ADR-0001: Content as Python Constants

## Status

Accepted

## Context

The MVP is a single marketing landing page. The project does not need a database, CMS, or admin workflow yet, but it does need clean separation between copy and templates.

## Decision

All public copy lives in `pages/content.py` as frozen dataclasses, tuples, and dictionaries. Templates only render these constants.

## Consequences

This keeps the presentation layer simple, testable, and easy to migrate later. If Above Board needs editorial workflows, the dataclasses can map cleanly to a CMS or database model without rewriting the templates.

