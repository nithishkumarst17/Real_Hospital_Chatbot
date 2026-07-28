from datetime import datetime, time
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from app.models import UserRole, AppointmentStatus

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    password: str = Field(min_length=6)
    preferred_language: str = "en"
    role: UserRole = UserRole.PATIENT


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    phone: Optional[str]
    role: UserRole
    preferred_language: str
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequest(BaseModel):
    refresh_token: str

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    qualification: Optional[str] = None
    languages_spoken: str = "en,ta"
    consultation_fee: int = 0
    available_days: str = "Mon,Tue,Wed,Thu,Fri"
    slot_start_time: time
    slot_end_time: time
    slot_duration_minutes: int = 15


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    qualification: Optional[str] = None
    languages_spoken: Optional[str] = None
    consultation_fee: Optional[int] = None
    available_days: Optional[str] = None
    slot_start_time: Optional[time] = None
    slot_end_time: Optional[time] = None
    slot_duration_minutes: Optional[int] = None
    is_active: Optional[bool] = None


class DoctorOut(BaseModel):
    id: str
    name: str
    specialization: str
    qualification: Optional[str]
    languages_spoken: str
    consultation_fee: int
    available_days: str
    slot_start_time: time
    slot_end_time: time
    slot_duration_minutes: int
    is_active: bool

    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    doctor_id: str
    appointment_date: datetime
    reason: Optional[str] = None
    language_used: str = "en"


class AppointmentUpdate(BaseModel):
    appointment_date: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    reason: Optional[str] = None


class AppointmentOut(BaseModel):
    id: str
    patient_id: str
    doctor_id: str
    appointment_date: datetime
    status: AppointmentStatus
    reason: Optional[str]
    language_used: str

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    detected_language: str
    detected_intent: str
    sources: Optional[List[str]] = None
