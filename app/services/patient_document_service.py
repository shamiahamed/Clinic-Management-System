import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi import UploadFile, status

from app.db.models.patient_model import Patient
from app.db.models.patient_document_model import PatientDocument
from app.exceptions.base_exception import BaseAppException
from app.exceptions.validation_exception import ValidationException

UPLOAD_BASE = "app/uploads/patients"

async def upload_patient_document(
    db: AsyncSession,
    patient_id: int,
    clinic_id: int,  # Added for security
    document_type: str,
    file: UploadFile,
    created_by: str
):
    # 1. VALIDATE OWNERSHIP (The most important part for your mentor)
    # This ensures the patient exists AND belongs to the clinic logged in
    query = select(Patient).where(
        and_(
            Patient.patient_id == patient_id,
            Patient.clinic_id == clinic_id
        )
    )
    result = await db.execute(query)
    patient = result.scalar_one_or_none()

    if not patient:
        raise BaseAppException(
            message=f"Access denied or Patient {patient_id} not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )

    # 2. VALIDATE FILE CONTENT
    content = await file.read()
    if not content:
        raise ValidationException(message="Uploaded file is empty.")

    # 3. FILE SYSTEM LOGIC
    patient_folder = os.path.join(UPLOAD_BASE, str(patient_id))
    os.makedirs(patient_folder, exist_ok=True)
    
    # Generate path and save
    file_path = os.path.join(patient_folder, file.filename)

    try:
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise BaseAppException(
            message=f"Disk write error: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # 4. DATABASE RECORD
    # created_at and updated_at are handled by AuditBaseModel automatically,
    # we pass created_by manually from our token info.
    document = PatientDocument(
        patient_id=patient_id,
        document_type=document_type,
        file_name=file.filename,
        file_path=file_path,
        created_by=created_by
    )

    db.add(document)
    await db.commit()
    await db.refresh(document)
    
    return document