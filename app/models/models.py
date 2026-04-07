import uuid
from datetime import datetime

from sqlalchemy import ARRAY, TIMESTAMP, Enum, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class PrinterProduct(Base):
    __tablename__ = "printer_product"
    __table_args__ = {"schema": "veoma"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str | None] = mapped_column(Text)
    whatsapp_number: Mapped[str | None] = mapped_column(Text)
    project_details: Mapped[str | None] = mapped_column(Text)
    file_url: Mapped[str | None] = mapped_column(Text)
    material: Mapped[str | None] = mapped_column(
        Enum("PLA", "PLA+", "ABS", "TPU", "PETG", name="material_enum", schema="veoma")
    )
    length_x: Mapped[float | None] = mapped_column(Numeric)
    width_y: Mapped[float | None] = mapped_column(Numeric)
    height_z: Mapped[float | None] = mapped_column(Numeric)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())


class Scanning(Base):
    __tablename__ = "scanning"
    __table_args__ = {"schema": "veoma"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    whatsapp_number: Mapped[str | None] = mapped_column(Text)
    email: Mapped[str | None] = mapped_column(Text)
    image_urls: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    project_details: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())


class Designing(Base):
    __tablename__ = "designing"
    __table_args__ = {"schema": "veoma"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    whatsapp_number: Mapped[str | None] = mapped_column(Text)
    email: Mapped[str | None] = mapped_column(Text)
    product_images: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    project_details: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())


class Feedback(Base):
    __tablename__ = "feedback"
    __table_args__ = {"schema": "veoma"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    profession: Mapped[str | None] = mapped_column(Text)
    message: Mapped[str | None] = mapped_column(Text)
    rating: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())


class WorkshopRegistration(Base):
    __tablename__ = "workshop_registration"
    __table_args__ = {"schema": "veoma"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    mobile_number: Mapped[str | None] = mapped_column(Text)
    email: Mapped[str | None] = mapped_column(Text)
    qualification: Mapped[str | None] = mapped_column(Text)
    workshop_name: Mapped[str | None] = mapped_column(
        Enum("Foundation", "Accelerator", "Online", name="workshop_name_enum", schema="veoma")
    )
    workshop_type: Mapped[str | None] = mapped_column(
        Enum("3d printing", "3d scanning", name="workshop_type_enum", schema="veoma")
    )
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())


class ContactMessage(Base):
    __tablename__ = "contact_messages"
    __table_args__ = {"schema": "veoma"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str | None] = mapped_column(Text)
    mobile_number: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(Text)
    user_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
