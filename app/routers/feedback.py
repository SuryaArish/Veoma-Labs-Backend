from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.models import Feedback
from app.schemas.schemas import FeedbackCreate, FeedbackResponse

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("", response_model=FeedbackResponse, status_code=201)
async def create_feedback(
    payload: FeedbackCreate, db: AsyncSession = Depends(get_db)
) -> Feedback:
    """Insert a new feedback entry."""
    record = Feedback(**payload.model_dump())
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


@router.get("", response_model=list[FeedbackResponse])
async def get_feedbacks(db: AsyncSession = Depends(get_db)) -> Sequence[Feedback]:
    """Fetch all feedback entries."""
    result = await db.execute(select(Feedback).order_by(Feedback.created_at.desc()))
    return result.scalars().all()
