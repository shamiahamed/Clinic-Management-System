from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime, String
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

class AuditBaseModel(Base):
    __abstract__ = True

    # Use lambda to get the current time at the moment of execution
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Store clinic_id/user info from the token
    created_by = Column(String, default="SYSTEM")
    updated_by = Column(String, default="SYSTEM")























# IMPORTANT: Manual registration of models so Base.metadata knows they exist
from app.db.models.clinic_model import Clinic
from app.db.models.doctor_model import Doctor
from app.db.models.patient_model import Patient
from app.db.models.appointment_model import Appointment
from app.db.models.patient_document_model import PatientDocument