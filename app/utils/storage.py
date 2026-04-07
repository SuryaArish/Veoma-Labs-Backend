import uuid

import httpx

from app.core import settings

_HEADERS = {"Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}"}


async def upload_image(bucket: str, file_bytes: bytes, content_type: str) -> str:
    """Upload a file to Supabase Storage and return its public URL.

    Args:
        bucket: Supabase storage bucket name.
        file_bytes: Raw file content.
        content_type: MIME type of the file (e.g. 'image/jpeg').

    Returns:
        Public URL of the uploaded file.
    """
    filename = f"{uuid.uuid4()}.{content_type.split('/')[-1]}"
    upload_url = f"{settings.SUPABASE_URL}/storage/v1/object/{bucket}/{filename}"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            upload_url,
            content=file_bytes,
            headers={**_HEADERS, "Content-Type": content_type},
        )
        response.raise_for_status()

    return f"{settings.SUPABASE_URL}/storage/v1/object/public/{bucket}/{filename}"
