import json
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.foundation import AuditEvent


class AuditService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def record(self, action: str, resource_type: str, actor_subject: str | None = None, resource_id: str | None = None, branch_id: str | None = None, metadata: dict | None = None) -> AuditEvent:
        event = AuditEvent(id=str(uuid4()), action=action, resource_type=resource_type, actor_subject=actor_subject, resource_id=resource_id, branch_id=branch_id, metadata_json=json.dumps(metadata or {}))
        self.db.add(event)
        await self.db.flush()
        return event
