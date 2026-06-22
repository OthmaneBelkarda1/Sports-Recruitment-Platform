import uuid
from pathlib import Path

from fastapi import UploadFile, HTTPException, status
from storage3.types import FileOptions
from supabase import create_client

from src.core.config import settings

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
ALLOWED_CV_EXTENSIONS = {".pdf", ".doc", ".docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

_CONTENT_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".pdf": "application/pdf",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

_supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
_bucket = settings.SUPABASE_STORAGE_BUCKET


def _validate_file(file: UploadFile, *, cv: bool = False) -> str:
    ext = Path(file.filename or "").suffix.lower()
    allowed = ALLOWED_CV_EXTENSIONS if cv else ALLOWED_EXTENSIONS
    if ext not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type '{ext}'. Allowed: {', '.join(sorted(allowed))}",
        )
    return ext


async def save_upload(file: UploadFile, prefix: str, *, cv: bool = False) -> str:
    ext = _validate_file(file, cv=cv)
    filename = f"{prefix}_{uuid.uuid4().hex}{ext}"

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large (max {MAX_FILE_SIZE // 1024 // 1024} MB)",
        )

    file_options = FileOptions({"content-type": _CONTENT_TYPES.get(ext, "application/octet-stream")})
    _supabase.storage.from_(_bucket).upload(filename, content, file_options)
    return _supabase.storage.from_(_bucket).get_public_url(filename)


async def delete_upload(url: str | None) -> None:
    if not url:
        return
    filename = url.rsplit("/", 1)[-1]
    try:
        _supabase.storage.from_(_bucket).remove([filename])
    except Exception:
        pass
