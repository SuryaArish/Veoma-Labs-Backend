from typing import Sequence

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.models import Designing
from app.schemas.schemas import DesigningCreate, DesigningResponse
from app.utils.email import send_submission_email

router = APIRouter(prefix="/designing", tags=["Designing"])


@router.post("", response_model=DesigningResponse, status_code=201)
async def create_designing(
    payload: DesigningCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> Designing:
    """Insert a new designing request."""
    record = Designing(**payload.model_dump())
    db.add(record)
    await db.commit()
    await db.refresh(record)
    background_tasks.add_task(send_submission_email, "3D Designing", payload.model_dump())
    return record

@router.get("", response_model=list[DesigningResponse])
async def get_designings(db: AsyncSession = Depends(get_db)) -> Sequence[Designing]:
    """Fetch all designing requests."""
    result = await db.execute(select(Designing).order_by(Designing.created_at.desc()))
    return result.scalars().all()
