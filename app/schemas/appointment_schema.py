from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class AppointmentStatus(str, Enum):
    BOOKED = "BOOKED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class AppointmentCreate(BaseModel):
    clinic_id: int
    doctor_id: int
    patient_id: int
    appointment_time: datetime


class AppointmentResponse(BaseModel):
    doctor_id: int
    appointment_id: int
    patient_id: int
    appointment_time: datetime
    appointment_status: AppointmentStatus

    class Config:
        from_attributes = True
