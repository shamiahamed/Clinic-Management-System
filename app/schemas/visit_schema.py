from pydantic import BaseModel
from datetime import datetime

class VisitCreate(BaseModel):
    clinic_id: int
    doctor_id: int
    appointment_time: datetime
