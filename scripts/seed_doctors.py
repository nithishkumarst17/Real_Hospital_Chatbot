"""
Populates the doctors table with sample data.
Run via: python -m scripts.seed_doctors
"""
from datetime import time
from app.database import SessionLocal, Base, engine
from app.models import Doctor

Base.metadata.create_all(bind=engine)

SAMPLE_DOCTORS = [
    dict(
        name="Anitha Raman", specialization="Cardiology",
        qualification="MD, DM Cardiology", languages_spoken="en,ta",
        consultation_fee=800, available_days="Mon,Wed,Fri",
        slot_start_time=time(9, 0), slot_end_time=time(13, 0),
        slot_duration_minutes=15,
    ),
    dict(
        name="Karthik Subramaniam", specialization="Orthopedics",
        qualification="MS Ortho", languages_spoken="en,ta",
        consultation_fee=600, available_days="Tue,Thu,Sat",
        slot_start_time=time(10, 0), slot_end_time=time(14, 0),
        slot_duration_minutes=20,
    ),
    dict(
        name="Priya Venkatesan", specialization="Pediatrics",
        qualification="MD Pediatrics", languages_spoken="en,ta",
        consultation_fee=500, available_days="Mon,Tue,Wed,Thu,Fri",
        slot_start_time=time(11, 0), slot_end_time=time(17, 0),
        slot_duration_minutes=15,
    ),
    dict(
        name="Suresh Kumar", specialization="General Medicine",
        qualification="MBBS, MD", languages_spoken="en,ta",
        consultation_fee=400, available_days="Mon,Tue,Wed,Thu,Fri,Sat",
        slot_start_time=time(9, 0), slot_end_time=time(18, 0),
        slot_duration_minutes=10,
    ),
]


def seed():
    db = SessionLocal()
    try:
        for doc_data in SAMPLE_DOCTORS:
            existing = db.query(Doctor).filter(Doctor.name == doc_data["name"]).first()
            if not existing:
                db.add(Doctor(**doc_data))
        db.commit()
        print(f"Seeded {len(SAMPLE_DOCTORS)} doctors (skipping any already present).")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
