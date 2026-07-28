from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Appointment, Doctor, User, UserRole, AppointmentStatus
from app.schemas import AppointmentCreate, AppointmentUpdate, AppointmentOut
from app.auth import get_current_user, require_roles
from app.email_service import send_appointment_confirmation, send_appointment_cancellation

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def book_appointment(
    payload: AppointmentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    doctor = db.query(Doctor).filter(Doctor.id == payload.doctor_id, Doctor.is_active == True).first()  # noqa: E712
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found or inactive")

    clash = db.query(Appointment).filter(
        Appointment.doctor_id == doctor.id,
        Appointment.appointment_date == payload.appointment_date,
        Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED]),
    ).first()
    if clash:
        raise HTTPException(status_code=409, detail="This slot is already booked")

    appointment = Appointment(
        patient_id=current_user.id,
        doctor_id=doctor.id,
        appointment_date=payload.appointment_date,
        reason=payload.reason,
        language_used=payload.language_used,
        status=AppointmentStatus.CONFIRMED,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    background_tasks.add_task(
        send_appointment_confirmation,
        to_email=current_user.email,
        patient_name=current_user.full_name,
        doctor_name=doctor.name,
        appointment_date=str(appointment.appointment_date),
        language=payload.language_used,
    )
    return appointment


@router.get("/me", response_model=List[AppointmentOut])
def my_appointments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Appointment).filter(Appointment.patient_id == current_user.id).all()


@router.get(
    "/", response_model=List[AppointmentOut],
    dependencies=[Depends(require_roles([UserRole.ADMIN, UserRole.RECEPTIONIST]))],
)
def all_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()


@router.patch("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(
    appointment_id: str,
    payload: AppointmentUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    is_owner = appointment.patient_id == current_user.id
    is_staff = current_user.role in (UserRole.ADMIN, UserRole.RECEPTIONIST)
    if not (is_owner or is_staff):
        raise HTTPException(status_code=403, detail="Not authorized to modify this appointment")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(appointment, field, value)
    db.commit()
    db.refresh(appointment)

    if payload.status == AppointmentStatus.CANCELLED:
        doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
        background_tasks.add_task(
            send_appointment_cancellation,
            to_email=current_user.email,
            patient_name=current_user.full_name,
            doctor_name=doctor.name if doctor else "N/A",
            appointment_date=str(appointment.appointment_date),
            language=appointment.language_used,
        )
    return appointment
