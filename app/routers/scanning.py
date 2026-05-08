from typing import Sequence

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.models import Scanning
from app.schemas.schemas import ScanningCreate, ScanningResponse
from app.utils.email import send_submission_email
from app.utils.storage import upload_image

router = APIRouter(prefix="/scanning", tags=["Scanning"])


@router.post("", response_model=ScanningResponse, status_code=201)
async def create_scanning(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    full_name: str = Form(...),
    whatsapp_number: str | None = Form(None),
    email: str | None = Form(None),
    project_details: str | None = Form(None),
    images: list[UploadFile] = File(default=[]),
) -> Scanning:
    """Accept multipart/form-data with optional image uploads."""
    image_urls: list[str] = []
    for img in images:
        if img.filename:
            content = await img.read()
            url = await upload_image("scanning", content, img.content_type or "image/jpeg", img.filename)
            image_urls.append(url)

    data = {
        "full_name": full_name,
        "whatsapp_number": whatsapp_number,
        "email": email,
        "project_details": project_details,
        "image_urls": image_urls or None,
    }
    record = Scanning(**data)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    background_tasks.add_task(send_submission_email, "3D Scanning", data)
    return record


@router.post("/json", response_model=ScanningResponse, status_code=201)
async def create_scanning_json(
    payload: ScanningCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> Scanning:
    """Accept application/json (image_urls already uploaded and passed directly)."""
    data = payload.model_dump()
    record = Scanning(**data)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    background_tasks.add_task(send_submission_email, "3D Scanning", data)
    return record


@router.get("", response_model=list[ScanningResponse])
async def get_scannings(db: AsyncSession = Depends(get_db)) -> Sequence[Scanning]:
    """Fetch all scanning requests."""
    result = await db.execute(select(Scanning).order_by(Scanning.created_at.desc()))
    return result.scalars().all()
