from fastapi import APIRouter, File, UploadFile

from app.utils.storage import upload_image

router = APIRouter(tags=["Upload"])


@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)) -> dict:
    """Upload a single file to Supabase Storage and return its public URL.

    The bucket is inferred from the file's MIME type:
    - image/* → 'designing' bucket (reused as generic image bucket)
    - everything else (STL, OBJ, etc.) → 'printer-product' bucket
    """
    content = await file.read()
    content_type = file.content_type or "application/octet-stream"
    bucket = "designing" if content_type.startswith("image/") else "printer-product"
    url = await upload_image(bucket, content, content_type, file.filename)
    return {"url": url}
