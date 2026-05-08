import uuid

import httpx

from app.core import settings

_SUPABASE_URL = settings.SUPABASE_URL.strip()
_HEADERS = {"Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}"}

# Maps MIME types that don't carry a useful extension to explicit extensions.
_MIME_TO_EXT: dict[str, str] = {
    "application/octet-stream": "",  # resolved from original filename instead
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
    "image/gif": "gif",
}


def _resolve_ext(original_filename: str | None, content_type: str) -> str:
    """Return the best file extension for the upload.

    Prefers the extension from the original filename; falls back to the MIME
    type mapping, then the subtype portion of the MIME type.
    """
    if original_filename and "." in original_filename:
        return original_filename.rsplit(".", 1)[-1].lower()
    mime_ext = _MIME_TO_EXT.get(content_type)
    if mime_ext is not None:
        return mime_ext
    return content_type.split("/")[-1].lower()


async def upload_file(
    bucket: str,
    file_bytes: bytes,
    content_type: str,
    original_filename: str | None = None,
) -> str:
    """Upload a file to Supabase Storage and return its public URL.

    Args:
        bucket: Supabase storage bucket name.
        file_bytes: Raw file content.
        content_type: MIME type of the file.
        original_filename: Original filename from the upload (used to preserve
            the extension for binary formats like STL/OBJ).

    Returns:
        Public URL of the uploaded file.
    """
    ext = _resolve_ext(original_filename, content_type)
    filename = f"{uuid.uuid4()}.{ext}" if ext else str(uuid.uuid4())
    upload_url = f"{_SUPABASE_URL}/storage/v1/object/{bucket}/{filename}"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            upload_url,
            content=file_bytes,
            headers={**_HEADERS, "Content-Type": content_type},
        )
        response.raise_for_status()

    return f"{_SUPABASE_URL}/storage/v1/object/public/{bucket}/{filename}"


# Backward-compatible alias used by existing routers.
upload_image = upload_file
