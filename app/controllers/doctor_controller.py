from sqlalchemy.ext.asyncio import AsyncSession
from app.services.doctor_service import (
    create_doctor,
    list_doctors,
    get_doctor_by_id,
    update_doctor
)


class DoctorController:

    @staticmethod
    async def create(db: AsyncSession, payload, created_by: str):
        return await create_doctor(
            db=db,
            clinic_id=payload.clinic_id,
            doctor_name=payload.doctor_name,
            specialization=payload.specialization,
            created_by=created_by
        )

    @staticmethod
    async def list(db: AsyncSession, clinic_id: int | None = None):
        return await list_doctors(db, clinic_id)

    @staticmethod
    async def get_by_id(db: AsyncSession, doctor_id: int):
        return await get_doctor_by_id(db, doctor_id)

    @staticmethod
    async def update(db: AsyncSession, doctor_id: int, payload, updated_by: str):
        return await update_doctor(
            db=db,
            doctor_id=doctor_id,
            doctor_name=payload.doctor_name,
            specialization=payload.specialization,
            is_active=payload.is_active,
            updated_by=updated_by
        )
