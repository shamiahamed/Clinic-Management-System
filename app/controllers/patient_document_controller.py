from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from app.services.patient_document_service import upload_patient_document


class PatientDocumentController:

    @staticmethod
    async def upload(
        db: AsyncSession,
        patient_id: int,
        clinic_id: int,  # to ensure security
        document_type: str,
        file: UploadFile,
        created_by: str
    ):
        # Passing all arguments to the service, including clinic_id
        return await upload_patient_document(
            db=db,
            patient_id=patient_id,
            clinic_id=clinic_id,
            document_type=document_type,
            file=file,
            created_by=created_by
        )