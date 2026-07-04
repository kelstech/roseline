from app.services.storage import DocumentStorageService


def test_document_storage_roundtrip(tmp_path):
    service = DocumentStorageService(str(tmp_path))
    key = service.put_bytes(b"clinical document", "note.txt")
    assert service.get_bytes(key) == b"clinical document"
