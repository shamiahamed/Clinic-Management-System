from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import AuditBaseModel

class PatientDocument(AuditBaseModel):
    __tablename__ = "patient_document"

    document_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)

    document_type = Column(String, nullable=False)  # ID_PROOF / REPORT
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)

    patient = relationship("Patient", backref="documents")
