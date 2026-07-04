from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.foundation import NotificationOutbox


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def enqueue(self, channel: str, recipient: str, body: str, subject: str | None = None) -> NotificationOutbox:
        message = NotificationOutbox(id=str(uuid4()), channel=channel, recipient=recipient, subject=subject, body=body)
        self.db.add(message)
        await self.db.flush()
        return message
