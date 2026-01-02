from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from fastapi import status

from app.db.models.appointment_model import Appointment
from app.schemas.appointment_schema import AppointmentCreate, AppointmentStatus

# --- IMPORT EXCEPTIONS ---
from app.exceptions.base_exception import BaseAppException
from app.exceptions.validation_exception import ValidationException

# CREATE
async def create_appointment(
    db: AsyncSession,
    payload: AppointmentCreate
):
    # Check for Double Booking
    query = select(Appointment).where(
        Appointment.doctor_id == payload.doctor_id,
        Appointment.appointment_time == payload.appointment_time,
        Appointment.appointment_status == AppointmentStatus.BOOKED
    )

    result = await db.execute(query)
    existing = result.scalar_one_or_none()

    if existing:
        # Validation Error
        raise ValidationException(f"Doctor ID {payload.doctor_id} already has an appointment at this time")

    appointment = Appointment(
        clinic_id=payload.clinic_id,
        doctor_id=payload.doctor_id,
        patient_id=payload.patient_id,
        appointment_time=payload.appointment_time,
        appointment_status=AppointmentStatus.BOOKED,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)
    return appointment


# GET ALL
async def get_all_appointments(db: AsyncSession):
    query = select(Appointment)
    result = await db.execute(query)
    appointments = result.scalars().all()
    
    if not appointments:
        raise BaseAppException(
            message="No appointments found in the system",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return appointments


# GET BY ID
async def get_appointment_by_id(
    db: AsyncSession,
    appointment_id: int
):
    query = select(Appointment).where(
        Appointment.appointment_id == appointment_id
    )
    result = await db.execute(query)
    appointment = result.scalar_one_or_none()

    if not appointment:
        #404 Error
        raise BaseAppException(
            message=f"Appointment with ID {appointment_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    return appointment


# GET BY DOCTOR
async def get_appointments_by_doctor(
    db: AsyncSession,
    doctor_id: int
):
    query = select(Appointment).where(
        Appointment.doctor_id == doctor_id
    )
    result = await db.execute(query)
    appointments = result.scalars().all()
    
    if not appointments:
        raise BaseAppException(
            message=f"No appointments found for Doctor ID {doctor_id}",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return appointments


# UPDATE STATUS
async def update_appointment_status(
    db: AsyncSession,
    appointment_id: int,
    new_status: AppointmentStatus,
    updated_by: str
):
    query = select(Appointment).where(
        Appointment.appointment_id == appointment_id
    )

    result = await db.execute(query)
    appointment = result.scalar_one_or_none()

    if not appointment:
        # 404 Error
        raise BaseAppException(
            message=f"Cannot update status. Appointment with ID {appointment_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    appointment.appointment_status = new_status
    appointment.updated_at = datetime.now(timezone.utc)
    appointment.updated_by = updated_by

    await db.commit()
    await db.refresh(appointment)
    return appointment