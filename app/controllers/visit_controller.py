from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from app.services.visit_service import create_patient_visit

class VisitController:

    @staticmethod
    async def create_visit(
        db: AsyncSession,
        patient_id: int,
        clinic_id: int,       # From Token for security
        doctor_id: int,
        appointment_time: any,
        documents: list[UploadFile],
        created_by: str       # e.g., "CLINIC_9"
    ):
        # Passes the secure data to the service layer
        return await create_patient_visit(
            db=db,
            patient_id=patient_id,
            clinic_id=clinic_id,
            doctor_id=doctor_id,
            appointment_time=appointment_time,
            documents=documents,
            created_by=created_by
        )