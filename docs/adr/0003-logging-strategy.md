# ADR-0003: Logging Strategy

## Status

Accepted

## Context

Developers need readable terminal output locally. Production needs structured logs that can be searched and shipped to systems such as Datadog, CloudWatch, or Loki.

## Decision

Development uses console-only human-readable logs. Production uses JSON logs written to both console and a rotating file at `logs/aboveboard.log`.

## Consequences

Local debugging stays simple, while production logs have stable fields for aggregation and alerting. File rotation keeps disk usage bounded.

