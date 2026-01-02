from pydantic import BaseModel
from enum import Enum

class PatientStatus(str, Enum):
    NEW = "NEW"
    ACTIVE = "ACTIVE"
    DISCHARGED = "DISCHARGED"

class PatientCreate(BaseModel):
    clinic_id: int
    patient_name: str
    phone_number: str

class PatientStatusUpdate(BaseModel):
    patient_status: PatientStatus

class PatientResponse(BaseModel):
    patient_id: int
    patient_name: str
    phone_number: str
    patient_status: str

    class Config:
        from_attributes = True


"""class PatientUploadResponse(BaseModel):
    status: str = "success"
    message: str
    data: Any

    class Config:
        from_attributes = True #for DB objects"""