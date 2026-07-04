from pathlib import Path
from uuid import uuid4
from app.core.config import get_settings


class DocumentStorageService:
    """Local storage adapter; production deployments can replace it with S3/Azure Blob/GCS."""

    def __init__(self, root: str | None = None):
        self.root = Path(root or get_settings().storage_local_path)
        self.root.mkdir(parents=True, exist_ok=True)

    def put_bytes(self, content: bytes, filename: str) -> str:
        safe_name = Path(filename).name
        key = f"{uuid4()}-{safe_name}"
        (self.root / key).write_bytes(content)
        return key

    def get_bytes(self, key: str) -> bytes:
        return (self.root / Path(key).name).read_bytes()
