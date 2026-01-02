from sqlalchemy.ext.asyncio import AsyncSession
from app.services.patient_service import (
    create_patient,
    list_patients,
    get_patient_by_id,
    update_patient_status
)

class PatientController:
    @staticmethod
    async def create(db: AsyncSession, payload, clinic_id: int, created_by: str):
        # SECURE: Use clinic_id passed from the Token (via Routes), not the payload
        return await create_patient(
            db=db,
            clinic_id=clinic_id, 
            patient_name=payload.patient_name,
            phone_number=payload.phone_number,
            created_by=created_by
        )

    @staticmethod
    async def list(db: AsyncSession, clinic_id: int):
        # clinic_id is now required to filter the list
        return await list_patients(db, clinic_id)

    @staticmethod
    async def get_by_id(db: AsyncSession, patient_id: int, clinic_id: int):
        # SECURE: Added clinic_id so service can check ownership
        return await get_patient_by_id(db, patient_id, clinic_id)

    @staticmethod
    async def update_status(db: AsyncSession, patient_id: int, payload, clinic_id: int, updated_by: str):
        # SECURE: Added clinic_id to ensure the clinic owns this patient before updating
        return await update_patient_status(
            db=db,
            patient_id=patient_id,
            clinic_id=clinic_id,
            new_status=payload.patient_status,
            updated_by=updated_by
        )