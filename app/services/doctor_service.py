from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from fastapi import status

from app.db.models.doctor_model import Doctor
from app.db.models.clinic_model import Clinic
from app.exceptions.base_exception import BaseAppException


# Create Doctor
async def create_doctor(
    db: AsyncSession,
    clinic_id: int,
    doctor_name: str,
    specialization: str,
    created_by: str
):
    # Validate clinic exists before adding doctor
    clinic_query = select(Clinic).where(
        Clinic.clinic_id == clinic_id,
        Clinic.is_active == True
    )
    clinic_result = await db.execute(clinic_query)
    clinic = clinic_result.scalar_one_or_none()

    if not clinic:
        # 404 Exception
        raise BaseAppException(
            message=f"Cannot add doctor. Clinic with ID {clinic_id} not found or inactive",
            status_code=status.HTTP_404_NOT_FOUND
        )

    # Create doctor
    doctor = Doctor(
        clinic_id=clinic_id,
        doctor_name=doctor_name,
        specialization=specialization,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        created_by=created_by,
        updated_by=created_by
    )

    db.add(doctor)
    await db.commit()
    await db.refresh(doctor)
    return doctor


# Get doctor by id
async def get_doctor_by_id(
    db: AsyncSession,
    doctor_id: int
):
    query = select(Doctor).where(
        Doctor.doctor_id == doctor_id,
        Doctor.is_active == True
    )

    result = await db.execute(query)
    doctor = result.scalar_one_or_none()

    if not doctor:
        # 404 Exception
        raise BaseAppException(
            message=f"Doctor with ID {doctor_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    return doctor


# Update doctors
async def update_doctor(
    db: AsyncSession,
    doctor_id: int,
    doctor_name: str | None,
    specialization: str | None,
    is_active: bool | None,
    updated_by: str
):
    query = select(Doctor).where(
        Doctor.doctor_id == doctor_id
    )
    result = await db.execute(query)
    doctor = result.scalar_one_or_none()

    if not doctor:
        # 404 Exception
        raise BaseAppException(
            message=f"Cannot update. Doctor with ID {doctor_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    if doctor_name is not None:
        doctor.doctor_name = doctor_name

    if specialization is not None:
        doctor.specialization = specialization

    if is_active is not None:
        doctor.is_active = is_active

    doctor.updated_at = datetime.now(timezone.utc)
    doctor.updated_by = updated_by

    await db.commit()
    await db.refresh(doctor)
    return doctor


# Updated List Doctors with Exception
async def list_doctors(
    db: AsyncSession,
    clinic_id: int | None = None
):
    query = select(Doctor).where(
        Doctor.is_active == True
    )

    if clinic_id:
        query = query.where(
            Doctor.clinic_id == clinic_id
        )

    result = await db.execute(query)
    doctors = result.scalars().all()

    # If the list is empty, throw a 404
    if not doctors:
        message = "No active doctors found"
        if clinic_id:
            message = f"No active doctors found for Clinic ID {clinic_id}"
            
        raise BaseAppException(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )

    return doctors