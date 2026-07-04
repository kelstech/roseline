# EHIS Module 01: Core Architecture & System Foundation

This repository contains the foundational platform for an Enterprise Hospital Information System (EHIS) serving a large, multi-branch cardiovascular and oncology hospital network.

## Module outputs
1. [Executive summary](docs/architecture.md#executive-summary)
2. [System architecture diagrams](docs/architecture.md#system-architecture-diagrams)
3. [Project folder structure](docs/developer-guide.md#project-folder-structure)
4. [Shared database design](docs/database.md)
5. [Common utilities and reusable services](docs/developer-guide.md#common-utilities-and-reusable-services)
6. [Authentication integration points](docs/security.md#authentication-integration-points)
7. [Logging, monitoring, and audit framework](docs/observability.md)
8. [Security framework and coding standards](docs/security.md)
9. [Global exception handling](docs/developer-guide.md#global-exception-handling)
10. [Notification infrastructure](docs/developer-guide.md#notification-infrastructure)
11. [File and document storage strategy](docs/storage.md)
12. [UI design system and reusable components](docs/ui-design-system.md)
13. [Environment configuration and secrets management](docs/deployment.md#environment-configuration-and-secrets-management)
14. [Docker and Kubernetes configuration](infra/)
15. [CI/CD pipeline](.github/workflows/ci.yml)
16. [Developer documentation](docs/developer-guide.md)
17. Production-ready foundational code in `backend/` and `frontend/`
18. Unit and integration tests in `backend/app/tests/`
19. [Deployment instructions](docs/deployment.md)

## Quick start

```bash
cp .env.example .env
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt -r backend/requirements-dev.txt
uvicorn app.main:app --app-dir backend --reload
```

## Testing

```bash
PYTHONPATH=backend pytest backend/app/tests
```
