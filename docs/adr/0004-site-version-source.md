# ADR-0004: Site Version Source

## Status

Accepted

## Context

The footer should show a version in development, but the portfolio project should not depend on Git metadata at runtime.

## Decision

Read the site version from the root `VERSION` file during `PagesConfig.ready()` and expose it through the site context processor.

## Consequences

The version source is explicit, portable, and honest. Deployments can update the file without relying on repository state inside the runtime image.

