import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime, timezone
from fastapi import UploadFile, status

from app.db.models.patient_model import Patient
from app.db.models.clinic_model import Clinic
from app.db.models.patient_document_model import PatientDocument
from app.schemas.patient_schema import PatientStatus
from app.exceptions.base_exception import BaseAppException
from app.exceptions.validation_exception import ValidationException

UPLOAD_BASE = "app/uploads/patients"

# Register patient
async def create_patient(db: AsyncSession, clinic_id: int, patient_name: str, phone_number: str, created_by: str):
    # Validate clinic belongs to this user/is active
    clinic_query = select(Clinic).where(and_(Clinic.clinic_id == clinic_id, Clinic.is_active == True))
    clinic_result = await db.execute(clinic_query)
    if not clinic_result.scalar_one_or_none():
        raise BaseAppException(message="Clinic not found or inactive", status_code=status.HTTP_404_NOT_FOUND)

    patient = Patient(
        clinic_id=clinic_id,
        patient_name=patient_name,
        phone_number=phone_number,
        patient_status=PatientStatus.NEW.value,
        created_by=created_by
    )
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    return patient

# LIST PATIENTS (Filtered by Clinic)
async def list_patients(db: AsyncSession, clinic_id: int):
    # SECURE: Always filter by clinic_id from token
    query = select(Patient).where(Patient.clinic_id == clinic_id)
    result = await db.execute(query)
    patients = result.scalars().all()
    
    if not patients:
        raise BaseAppException(message="No patients found for your clinic", status_code=status.HTTP_404_NOT_FOUND)
    return patients

# GET PATIENT BY ID (Secure)
async def get_patient_by_id(db: AsyncSession, patient_id: int, clinic_id: int):
    query = select(Patient).where(and_(Patient.patient_id == patient_id, Patient.clinic_id == clinic_id))
    result = await db.execute(query)
    patient = result.scalar_one_or_none()
    
    if not patient:
        raise BaseAppException(message="Patient not found or access denied", status_code=status.HTTP_404_NOT_FOUND)
    return patient

# UPDATE STATUS (Secure)
async def update_patient_status(db: AsyncSession, patient_id: int, clinic_id: int, new_status: str, updated_by: str):
    patient = await get_patient_by_id(db, patient_id, clinic_id)
    patient.patient_status = new_status
    patient.updated_by = updated_by
    await db.commit()
    await db.refresh(patient)
    return patient