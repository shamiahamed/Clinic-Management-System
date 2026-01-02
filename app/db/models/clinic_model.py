from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import AuditBaseModel

class Clinic(AuditBaseModel):
    __tablename__ = "clinic"

    clinic_id = Column(Integer, primary_key=True, index=True)
    clinic_name = Column(String, nullable=False)
    clinic_address = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
