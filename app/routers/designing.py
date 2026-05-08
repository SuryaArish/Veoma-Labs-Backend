from typing import Optional, Sequence

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.models import Designing
from app.schemas.schemas import DesigningResponse
from app.utils.email import send_submission_email
from app.utils.storage import upload_image

router = APIRouter(prefix="/designing", tags=["Designing"])


@router.post("", response_model=DesigningResponse, status_code=201)
async def create_designing(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    full_name: str = Form(...),
    email: Optional[str] = Form(None),
    whatsapp_number: Optional[str] = Form(None),
    project_details: Optional[str] = Form(None),
    images: list[UploadFile] = File(default=[]),
) -> Designing:
    """Insert a new designing request, uploading product images to Supabase Storage."""
    product_images: list[str] = []
    for img in images:
        content = await img.read()
        url = await upload_image("designing", content, img.content_type or "image/jpeg", img.filename)
        product_images.append(url)

    data = {
        "full_name": full_name,
        "email": email,
        "whatsapp_number": whatsapp_number,
        "project_details": project_details,
        "product_images": product_images or None,
    }
    record = Designing(**data)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    background_tasks.add_task(send_submission_email, "3D Designing", data)
    return record


@router.get("", response_model=list[DesigningResponse])
async def get_designings(db: AsyncSession = Depends(get_db)) -> Sequence[Designing]:
    """Fetch all designing requests."""
    result = await db.execute(select(Designing).order_by(Designing.created_at.desc()))
    return result.scalars().all()
