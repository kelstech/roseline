# Deployment instructions

## Environment configuration and secrets management
- Copy `.env.example` for local development only.
- In Kubernetes, store non-secret configuration in `ConfigMap` and secrets in `Secret` or an external secret manager.
- Rotate database, object storage, and notification provider credentials regularly.

## Docker
```bash
docker build -f infra/docker/backend.Dockerfile -t ehis-core-backend .
docker run --env-file .env -p 8000:8000 ehis-core-backend
```

## Kubernetes
```bash
kubectl apply -f infra/k8s/namespace.yaml
kubectl apply -f infra/k8s/backend.yaml
```

## Production checklist
- Managed PostgreSQL configured and backed up.
- TLS ingress and WAF enabled.
- Object storage encryption, retention, and malware scanning enabled.
- Central logs, metrics, alerts, and audit retention enabled.
- CI/CD gates pass before release promotion.
