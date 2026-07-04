# Security framework and coding standards

## Authentication integration points
Authentication is intentionally not enforced in Module 01. API dependencies expose a `Principal` contract and an `optional_principal` seam where future OIDC/JWT validation will be implemented.

## Standards
- Never log PHI, credentials, access tokens, or full documents.
- Use parameterized ORM queries only.
- Validate all settings with typed configuration.
- Use branch-aware authorization in every future clinical module.
- Require TLS at ingress and encrypted managed storage in production.
- Apply least-privilege service accounts and short-lived credentials.
- Do not wrap imports in `try/except`; dependency errors must fail fast.
