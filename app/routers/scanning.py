from typing import Sequence

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.models import Scanning
from app.schemas.schemas import ScanningCreate, ScanningResponse
from app.utils.email import send_submission_email

router = APIRouter(prefix="/scanning", tags=["Scanning"])


@router.post("", response_model=ScanningResponse, status_code=201)
async def create_scanning(
    payload: ScanningCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> Scanning:
    """Insert a new scanning request."""
    record = Scanning(**payload.model_dump())
    db.add(record)
    await db.commit()
    await db.refresh(record)
    background_tasks.add_task(send_submission_email, "3D Scanning", payload.model_dump())
    return record


@router.get("", response_model=list[ScanningResponse])
async def get_scannings(db: AsyncSession = Depends(get_db)) -> Sequence[Scanning]:
    """Fetch all scanning requests."""
    result = await db.execute(select(Scanning).order_by(Scanning.created_at.desc()))
    return result.scalars().all()
