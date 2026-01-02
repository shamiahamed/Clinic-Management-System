from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClinicCreate(BaseModel):
    clinic_name: str
    clinic_address: str


class ClinicResponse(BaseModel):
    clinic_id: int      
    clinic_name: str
    clinic_address: str
    

    class Config:
        from_attributes = True
