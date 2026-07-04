# Developer guide

## Project folder structure

```text
backend/app/api/v1        Versioned HTTP routers
backend/app/core          Config, logging, middleware, security seams, exceptions
backend/app/db            Database base and session factory
backend/app/models        Shared database models
backend/app/services      Reusable domain/infrastructure services
backend/app/tests         Unit and integration tests
frontend/src/components   Reusable UI components
frontend/src/design       Design tokens
frontend/src/services     API clients
infra/docker              Container assets
infra/k8s                 Kubernetes manifests
```

## Common utilities and reusable services
- `Settings` provides typed environment configuration.
- `CorrelationIdMiddleware` propagates `x-correlation-id` and response timing.
- `AuditService` records durable audit events.
- `NotificationService` writes to an outbox for asynchronous delivery.
- `DocumentStorageService` abstracts file storage behind a replaceable adapter.

## Global exception handling
All application exceptions should use `EHISException` with stable error codes. Unhandled exceptions are logged with correlation IDs and returned as generic `internal_error` responses.

## Notification infrastructure
Module 01 implements the outbox persistence pattern. Delivery workers can later poll `core_notification_outbox` and send through approved email/SMS/push gateways while preserving retry state and auditability.
