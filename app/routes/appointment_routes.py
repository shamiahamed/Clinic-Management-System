from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.controllers.appointment_controller import AppointmentController
from app.schemas.appointment_schema import AppointmentCreate, AppointmentStatus, AppointmentResponse

router = APIRouter(prefix="/appointments", tags=["Appointment"])

@router.post("", response_model= AppointmentResponse)
async def book_appointment(
    payload: AppointmentCreate,
    db: AsyncSession = Depends(get_db)
):
    return await AppointmentController.create(
        db=db,
        payload=payload,
    )


@router.get("", response_model= List[AppointmentResponse])
async def view_appointments(db: AsyncSession = Depends(get_db)):
    return await AppointmentController.list(db)


@router.put("/{id}/status",response_model= AppointmentResponse)
async def update_status(
    id: int,
    status: AppointmentStatus,
    db: AsyncSession = Depends(get_db)
):
    return await AppointmentController.update_status(
        db=db,
        appointment_id=id,
        new_status=status,
        updated_by="system"
    )

