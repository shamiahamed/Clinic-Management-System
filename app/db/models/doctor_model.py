from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import AuditBaseModel

class Doctor(AuditBaseModel):
    __tablename__ = "doctor"

    doctor_id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, ForeignKey("clinic.clinic_id"), nullable=False)

    doctor_name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    clinic = relationship("Clinic", backref="doctors")
