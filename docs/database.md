# Shared database design and foundational tables

The foundation uses SQLAlchemy models with deterministic naming conventions for migration-safe relational schemas.

## Foundational tables
| Table | Purpose |
| --- | --- |
| `core_branches` | Hospital branches, time zones, activation state. |
| `core_audit_events` | Immutable audit trail for user/system actions. |
| `core_notification_outbox` | Durable queue for email/SMS/push/in-app notifications. |

## Design principles
- Every clinical module must reference `branch_id` for branch-aware access control and reporting.
- Protected health information should be minimized in audit metadata and logs.
- Future migrations should be managed with Alembic and reviewed for backward compatibility.
