from sqlalchemy.ext.asyncio import AsyncSession

from app.services.clinic_service import (
    create_clinic,
    get_clinic_by_id,
    list_clinics,
    update_clinic
)

class ClinicController:

    @staticmethod
    async def create(
        db: AsyncSession,
        payload,
        created_by: str
    ):
        return await create_clinic(
            db=db,
            clinic_name=payload.clinic_name,
            clinic_address=payload.clinic_address,
            created_by=created_by
        )
    
    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        clinic_id: int
    ):
        return await get_clinic_by_id(
            db=db,
            clinic_id=clinic_id
        )
    

    @staticmethod
    async def list(
        db: AsyncSession
    ):
        return await list_clinics(db)
    

    @staticmethod
    async def update(
        db: AsyncSession,
        clinic_id: int,
        payload,
        updated_by: str
    ):
        return await update_clinic(
            db=db,
            clinic_id=clinic_id,
            clinic_name=payload.clinic_name,
            clinic_address=payload.clinic_address,
            is_active=payload.is_active,
            updated_by=updated_by
        )


