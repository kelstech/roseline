# Architecture

## Executive summary
EHIS Module 01 establishes a modular, API-first foundation for multi-branch hospital operations. The platform separates clinical/business modules from cross-cutting infrastructure: configuration, auditability, observability, security seams, document storage, notifications, and reusable UI components. It is designed for cardiovascular and oncology workflows that require high availability, traceability, branch-aware data partitioning, regulated data handling, and integration with future identity, EMR, LIS, RIS/PACS, billing, and patient engagement services.

## System architecture diagrams

### Logical architecture
```mermaid
flowchart LR
  Users[Clinicians, Admins, Patients] --> Web[EHIS Web App]
  Web --> API[Core API Gateway / FastAPI]
  API --> Auth[OIDC/JWT Integration Point]
  API --> Core[Core Services: Audit, Notification, Storage]
  API --> Modules[Future Clinical Modules]
  Core --> DB[(Shared Relational DB)]
  Core --> ObjectStore[(Document/Object Storage)]
  Core --> Msg[Notification Outbox / Broker]
  API --> Observability[Logs, Metrics, Traces]
```

### Physical architecture
```mermaid
flowchart TB
  LB[Ingress / Load Balancer] --> FE[Frontend Pods]
  LB --> BE[Backend API Pods]
  BE --> PG[(Managed PostgreSQL)]
  BE --> S3[(S3-compatible Object Storage)]
  BE --> Redis[(Future Cache/Queue)]
  BE --> Prom[Prometheus]
  Prom --> Grafana[Grafana]
  BE --> Logs[Central Log Platform]
  Secrets[Kubernetes Secrets / External Secrets] --> BE
```
