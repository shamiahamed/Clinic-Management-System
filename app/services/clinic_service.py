from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone

from app.db.models.clinic_model import Clinic

from app.exceptions.validation_exception import ValidationException

# CREATE CLINIC
async def create_clinic(
    db: AsyncSession,
    clinic_name: str,
    clinic_address: str,
    created_by: str
):
    # Check if clinic name already exists
    query = select(Clinic).where(Clinic.clinic_name == clinic_name)
    result = await db.execute(query)
    existing_clinic = result.scalar_one_or_none()

    if existing_clinic:
        # Raise ValidationException if name exists
        raise ValidationException(
            message=f"A clinic with the name '{clinic_name}' already exists."
        )

    # If not exists, create it
    clinic = Clinic(
        clinic_name=clinic_name,
        clinic_address=clinic_address,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        created_by=created_by,
        updated_by=created_by
    )

    db.add(clinic)
    await db.commit()
    await db.refresh(clinic)

    return clinic


# GET CLINIC BY ID
async def get_clinic_by_id(
    db: AsyncSession,
    clinic_id: int
):
    query = select(Clinic).where(
        Clinic.clinic_id == clinic_id,
        Clinic.is_active == True
    )

    result = await db.execute(query)
    clinic = result.scalar_one_or_none()

    if not clinic:
        raise Exception("Clinic not found")

    return clinic


#LIST CLINICS
async def list_clinics(db: AsyncSession):
    query = select(Clinic).where(
        Clinic.is_active == True
    )

    result = await db.execute(query)
    return result.scalars().all()


#UPDATE CLINIC DETAILS
async def update_clinic(
    db: AsyncSession,
    clinic_id: int,
    clinic_name: str | None,
    clinic_address: str | None,
    is_active: bool | None,
    updated_by: str
):
    
    query = select(Clinic).where(
        Clinic.clinic_id == clinic_id
    )
    result = await db.execute(query)
    clinic = result.scalar_one_or_none()

    if not clinic:
        raise Exception("Clinic not found")

    # Update only provided fields
    if clinic_name is not None:
        clinic.clinic_name = clinic_name

    if clinic_address is not None:
        clinic.clinic_address = clinic_address

    if is_active is not None:
        clinic.is_active = is_active

    clinic.updated_at = datetime.now(timezone.utc)
    clinic.updated_by = updated_by

    await db.commit()
    await db.refresh(clinic)

    return clinic
