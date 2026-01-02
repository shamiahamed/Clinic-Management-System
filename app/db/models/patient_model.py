from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import AuditBaseModel

class Patient(AuditBaseModel):
    __tablename__ = "patient"

    patient_id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, ForeignKey("clinic.clinic_id"), nullable=False)

    patient_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    patient_status = Column(String, default="NEW")

    clinic = relationship("Clinic", backref="patients")
