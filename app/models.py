import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, ForeignKey, Enum, Text, Time
)

from sqlalchemy.orm import relationship

from app.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    RECEPTIONIST = "receptionist"
    DOCTOR = "doctor"
    PATIENT = "patient"


class AppointmentStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.PATIENT, nullable=False)
    preferred_language = Column(String(10), default="en")  # "en" or "ta"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    appointments = relationship(
        "Appointment", back_populates="patient",
        foreign_keys="Appointment.patient_id"
    )
    doctor_profile = relationship("Doctor", back_populates="user", uselist=False)


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    name = Column(String(150), nullable=False)
    specialization = Column(String(150), nullable=False, index=True)
    qualification = Column(String(255), nullable=True)
    languages_spoken = Column(String(100), default="en,ta")
    consultation_fee = Column(Integer, default=0)
    available_days = Column(String(50), default="Mon,Tue,Wed,Thu,Fri")  # CSV
    slot_start_time = Column(Time, nullable=False)
    slot_end_time = Column(Time, nullable=False)
    slot_duration_minutes = Column(Integer, default=15)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="doctor_profile")
    appointments = relationship("Appointment", back_populates="doctor")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    patient_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    doctor_id = Column(String(36), ForeignKey("doctors.id"), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.PENDING)
    reason = Column(Text, nullable=True)
    language_used = Column(String(10), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = relationship("User", back_populates="appointments", foreign_keys=[patient_id])
    doctor = relationship("Doctor", back_populates="appointments")


class ChatLog(Base):
    """Stores conversation turns for analytics / auditing / multi-turn context."""
    __tablename__ = "chat_logs"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    session_id = Column(String(100), index=True, nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    user_message = Column(Text, nullable=False)
    detected_language = Column(String(10), nullable=True)
    detected_intent = Column(String(50), nullable=True)
    assistant_response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
