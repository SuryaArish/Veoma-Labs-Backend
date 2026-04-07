import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


class MaterialEnum(str, Enum):
    PLA = "PLA"
    PLA_PLUS = "PLA+"
    ABS = "ABS"
    TPU = "TPU"
    PETG = "PETG"


class PrinterProductCreate(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    whatsapp_number: Optional[str] = None
    project_details: Optional[str] = None
    file_url: Optional[str] = None
    material: Optional[MaterialEnum] = None
    length_x: Optional[float] = None
    width_y: Optional[float] = None
    height_z: Optional[float] = None


class PrinterProductResponse(PrinterProductCreate):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Scanning ──────────────────────────────────────────────────────────────────

class ScanningCreate(BaseModel):
    full_name: str
    whatsapp_number: Optional[str] = None
    email: Optional[EmailStr] = None
    image_urls: Optional[list[str]] = None
    project_details: Optional[str] = None


class ScanningResponse(ScanningCreate):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Designing ─────────────────────────────────────────────────────────────────

class DesigningCreate(BaseModel):
    full_name: str
    whatsapp_number: Optional[str] = None
    email: Optional[EmailStr] = None
    product_images: Optional[list[str]] = None
    project_details: Optional[str] = None


class DesigningResponse(DesigningCreate):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Feedback ──────────────────────────────────────────────────────────────────

class FeedbackCreate(BaseModel):
    name: str
    profession: Optional[str] = None
    message: Optional[str] = None
    rating: Optional[int] = None

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not (1 <= v <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return v


class FeedbackResponse(FeedbackCreate):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Workshop Registration ─────────────────────────────────────────────────────

class WorkshopNameEnum(str, Enum):
    FOUNDATION = "Foundation"
    ACCELERATOR = "Accelerator"
    ONLINE = "Online"


class WorkshopTypeEnum(str, Enum):
    PRINTING = "3d printing"
    SCANNING = "3d scanning"


class WorkshopRegistrationCreate(BaseModel):
    full_name: str
    mobile_number: Optional[str] = None
    email: Optional[EmailStr] = None
    qualification: Optional[str] = None
    workshop_name: Optional[WorkshopNameEnum] = None
    workshop_type: Optional[WorkshopTypeEnum] = None


class WorkshopRegistrationResponse(WorkshopRegistrationCreate):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Contact Message ───────────────────────────────────────────────────────────

class ContactMessageCreate(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    mobile_number: Optional[str] = None
    location: Optional[str] = None
    user_message: Optional[str] = None


class ContactMessageResponse(ContactMessageCreate):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
