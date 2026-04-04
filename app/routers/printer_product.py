from typing import Sequence

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.models import PrinterProduct
from app.schemas.schemas import PrinterProductCreate, PrinterProductResponse
from app.utils.email import send_submission_email

router = APIRouter(prefix="/printer-product", tags=["Printer Product"])


@router.post("", response_model=PrinterProductResponse, status_code=201)
async def create_printer_product(
    payload: PrinterProductCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> PrinterProduct:
    """Insert a new printer product request."""
    record = PrinterProduct(**payload.model_dump())
    db.add(record)
    await db.commit()
    await db.refresh(record)
    background_tasks.add_task(send_submission_email, "3D Printer Product", payload.model_dump())
    return record


@router.get("", response_model=list[PrinterProductResponse])
async def get_printer_products(db: AsyncSession = Depends(get_db)) -> Sequence[PrinterProduct]:
    """Fetch all printer product requests."""
    result = await db.execute(select(PrinterProduct).order_by(PrinterProduct.created_at.desc()))
    return result.scalars().all()
