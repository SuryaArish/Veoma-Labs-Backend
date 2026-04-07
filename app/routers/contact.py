from typing import Sequence

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.models import ContactMessage
from app.schemas.schemas import ContactMessageCreate, ContactMessageResponse
from app.utils.email import send_submission_email

router = APIRouter(prefix="/contact", tags=["Contact"])


@router.post("", response_model=ContactMessageResponse, status_code=201)
async def create_contact_message(
    payload: ContactMessageCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> ContactMessage:
    """Insert a new contact message."""
    record = ContactMessage(**payload.model_dump())
    db.add(record)
    await db.commit()
    await db.refresh(record)
    background_tasks.add_task(send_submission_email, "Contact Message", payload.model_dump())
    return record


@router.get("", response_model=list[ContactMessageResponse])
async def get_contact_messages(db: AsyncSession = Depends(get_db)) -> Sequence[ContactMessage]:
    """Fetch all contact messages."""
    result = await db.execute(select(ContactMessage).order_by(ContactMessage.created_at.desc()))
    return result.scalars().all()
