from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.controllers.doctor_controller import DoctorController
from app.controllers.appointment_controller import AppointmentController
from app.schemas.doctor_schema import DoctorCreate, DoctorResponse
from app.schemas.appointment_schema import AppointmentResponse

router = APIRouter(prefix="/doctors", tags=["Doctor"])

@router.post("", response_model=DoctorResponse)
async def add_doctor(
    payload: DoctorCreate,
    db: AsyncSession = Depends(get_db)
):
    return await DoctorController.create(
        db=db,
        payload=payload,
        created_by="admin"
    )


@router.get("",response_model=List[DoctorResponse])
async def list_doctors(
    clinic_id: int | None = None,
    db: AsyncSession = Depends(get_db)
):
    return await DoctorController.list(db, clinic_id)



@router.get("/{doctor_id}/appointments", response_model=List[AppointmentResponse])
async def doctor_appointments(
    doctor_id: int, 
    db: AsyncSession = Depends(get_db)
):
    # This searches the 3rd column of your appointment table
    return await AppointmentController.get_by_doctor(
        db=db,
        doctor_id=doctor_id
    )