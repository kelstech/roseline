# Logging, monitoring, and audit framework

- Logs are structured JSON for aggregation and include correlation IDs.
- `/metrics` exposes Prometheus-compatible metrics.
- `/api/v1/healthz` and `/api/v1/readyz` support liveness and readiness probes.
- `AuditService` records actor, action, resource type, resource ID, branch, and metadata.
- Future tracing should propagate W3C trace context from ingress through downstream services.
