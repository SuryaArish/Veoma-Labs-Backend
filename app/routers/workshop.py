import asyncio
from typing import Sequence

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.models import WorkshopRegistration
from app.schemas.schemas import WorkshopRegistrationCreate, WorkshopRegistrationResponse
from app.utils.email import send_submission_email

router = APIRouter(prefix="/workshop", tags=["Workshop"])


@router.post("", response_model=WorkshopRegistrationResponse, status_code=201)
async def create_workshop_registration(
    payload: WorkshopRegistrationCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> WorkshopRegistration:
    """Insert a new workshop registration."""
    record = WorkshopRegistration(**payload.model_dump())
    db.add(record)
    await db.commit()
    await db.refresh(record)
    background_tasks.add_task(send_submission_email, "Workshop Registration", payload.model_dump())
    return record


@router.get("", response_model=list[WorkshopRegistrationResponse])
async def get_workshop_registrations(db: AsyncSession = Depends(get_db)) -> Sequence[WorkshopRegistration]:
    """Fetch all workshop registrations."""
    result = await db.execute(
        select(WorkshopRegistration).order_by(WorkshopRegistration.created_at.desc())
    )
    return result.scalars().all()
