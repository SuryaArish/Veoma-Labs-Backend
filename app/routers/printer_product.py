from typing import Optional, Sequence

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.models import PrinterProduct
from app.schemas.schemas import PrinterProductCreate, PrinterProductResponse
from app.utils.email import send_submission_email
from app.utils.storage import upload_image

router = APIRouter(prefix="/printer-product", tags=["Printer Product"])


@router.post("", response_model=PrinterProductResponse, status_code=201)
async def create_printer_product(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    full_name: str = Form(...),
    email: Optional[str] = Form(None),
    whatsapp_number: Optional[str] = Form(None),
    project_details: Optional[str] = Form(None),
    material: Optional[str] = Form(None),
    length_x: Optional[float] = Form(None),
    width_y: Optional[float] = Form(None),
    height_z: Optional[float] = Form(None),
    file: Optional[UploadFile] = File(None),
) -> PrinterProduct:
    """Accept multipart/form-data (with optional file upload)."""
    file_url: Optional[str] = None
    if file and file.filename:
        content = await file.read()
        file_url = await upload_image(
            "printer-product",
            content,
            file.content_type or "application/octet-stream",
            file.filename,
        )

    data = {
        "full_name": full_name,
        "email": email,
        "whatsapp_number": whatsapp_number,
        "project_details": project_details,
        "material": material,
        "length_x": length_x,
        "width_y": width_y,
        "height_z": height_z,
        "file_url": file_url,
    }
    record = PrinterProduct(**data)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    background_tasks.add_task(send_submission_email, "3D Printer Product", data)
    return record


@router.post("/json", response_model=PrinterProductResponse, status_code=201)
async def create_printer_product_json(
    payload: PrinterProductCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> PrinterProduct:
    """Accept application/json (file already uploaded; file_url passed directly)."""
    data = payload.model_dump()
    record = PrinterProduct(**data)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    background_tasks.add_task(send_submission_email, "3D Printer Product", data)
    return record


@router.get("", response_model=list[PrinterProductResponse])
async def get_printer_products(db: AsyncSession = Depends(get_db)) -> Sequence[PrinterProduct]:
    """Fetch all printer product requests."""
    result = await db.execute(select(PrinterProduct).order_by(PrinterProduct.created_at.desc()))
    return result.scalars().all()
