from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import AuditBaseModel

class Appointment(AuditBaseModel):
    __tablename__ = "appointment"

    appointment_id = Column(Integer, primary_key=True, index=True)

    clinic_id = Column(Integer, ForeignKey("clinic.clinic_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor.doctor_id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)

    appointment_time = Column(DateTime, default=datetime.utcnow)
    appointment_status = Column(String, default="BOOKED")

    clinic = relationship("Clinic", backref="appointments")
    doctor = relationship("Doctor", backref="appointments")
    patient = relationship("Patient", backref="appointments")
