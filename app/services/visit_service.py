import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi import UploadFile, status
from datetime import datetime, timezone

from app.db.models.patient_model import Patient
from app.db.models.appointment_model import Appointment
from app.db.models.patient_document_model import PatientDocument
from app.schemas.appointment_schema import AppointmentStatus
from app.exceptions.base_exception import BaseAppException
from app.exceptions.validation_exception import ValidationException

UPLOAD_BASE = "app/uploads/patients"

async def create_patient_visit(db: AsyncSession, patient_id: int, clinic_id: int, doctor_id: int, appointment_time: any, documents: list[UploadFile], created_by: str):
    # 1. Date Conversion
    if isinstance(appointment_time, str):
        try:
            appointment_time = datetime.fromisoformat(appointment_time.replace("Z", ""))
        except ValueError:
            raise ValidationException("Invalid date format.")

    # 2. Transaction Start
    async with db.begin():
        # SECURE: Check if patient exists AND belongs to this clinic
        res = await db.execute(select(Patient).where(and_(Patient.patient_id == patient_id, Patient.clinic_id == clinic_id)))
        patient = res.scalar_one_or_none()
        if not patient:
            raise BaseAppException(message="Patient access denied", status_code=status.HTTP_404_NOT_FOUND)

        # 3. Double Booking Check
        conflict = await db.execute(select(Appointment).where(and_(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_time == appointment_time,
            Appointment.appointment_status == AppointmentStatus.BOOKED
        )))
        if conflict.scalars().first():
            raise ValidationException(message="Doctor already booked at this time")

        # 4. Audit & Appointment
        patient.patient_status = "ACTIVE"
        patient.updated_by = created_by

        appointment = Appointment(
            clinic_id=clinic_id,
            doctor_id=doctor_id,
            patient_id=patient_id,
            appointment_time=appointment_time,
            appointment_status=AppointmentStatus.BOOKED,
            created_by=created_by,
            updated_by=created_by
        )
        db.add(appointment)

        # 5. Documents
        patient_folder = os.path.join(UPLOAD_BASE, str(patient_id))
        os.makedirs(patient_folder, exist_ok=True)

        for file in documents:
            file_path = os.path.join(patient_folder, file.filename)
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)

            db.add(PatientDocument(
                patient_id=patient_id,
                document_type="VISIT_DOC",
                file_name=file.filename,
                file_path=file_path,
                created_by=created_by
            ))

    return {"status": "success", "message": "Visit created", "clinic_admin": created_by}