from pydantic import BaseModel
from datetime import datetime

class DoctorCreate(BaseModel):
    clinic_id: int
    doctor_name: str
    specialization: str


class DoctorResponse(BaseModel):
    
    doctor_name: str
    specialization: str
   

    class Config:
        from_attributes = True
