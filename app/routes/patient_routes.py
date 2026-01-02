from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.controllers.visit_controller import VisitController
from app.controllers.patient_document_controller import PatientDocumentController
from app.db.session import get_db
from app.controllers.patient_controller import PatientController
from app.schemas.patient_schema import PatientCreate, PatientStatusUpdate, PatientResponse
from app.dependencies.authorization_dependency import get_current_clinic

router = APIRouter(
    prefix="/patients", 
    tags=["Patient"]
)

@router.post("", response_model=PatientResponse)
async def register_patient(
    payload: PatientCreate,
    db: AsyncSession = Depends(get_db),
    current_clinic: dict = Depends(get_current_clinic)
):
    return await PatientController.create(
        db=db,
        payload=payload,
        clinic_id=current_clinic["clinic_id"], # Passed for security
        created_by=f"CLINIC_{current_clinic['clinic_id']}"
    )

@router.get("", response_model=list[PatientResponse])
async def list_patients(
    db: AsyncSession = Depends(get_db),
    current_clinic: dict = Depends(get_current_clinic)
):
    return await PatientController.list(
        db=db, 
        clinic_id=current_clinic["clinic_id"]
    )

@router.put("/{id}/status", response_model=PatientResponse)
async def update_patient_status(
    id: int,
    payload: PatientStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_clinic: dict = Depends(get_current_clinic)
):
    return await PatientController.update_status(
        db=db,
        patient_id=id,
        payload=payload,
        clinic_id=current_clinic["clinic_id"], # Passed to verify ownership
        updated_by=f"CLINIC_{current_clinic['clinic_id']}"
    )

@router.post("/{id}/documents")
async def upload_patient_document(
    id: int,
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_clinic: dict = Depends(get_current_clinic)
):
    return await PatientDocumentController.upload(
        db=db,
        patient_id=id,
        clinic_id=current_clinic["clinic_id"], # Passed for security check
        document_type=document_type,
        file=file,
        created_by=f"CLINIC_{current_clinic['clinic_id']}"
    )

@router.post("/{id}/visit")
async def create_visit(
    id: int,
    doctor_id: int = Form(...),
    appointment_time: str = Form(...),
    documents: list[UploadFile] = File(...), 
    db: AsyncSession = Depends(get_db),
    current_clinic: dict = Depends(get_current_clinic)
):
    return await VisitController.create_visit(
        db=db,
        patient_id=id,
        clinic_id=current_clinic["clinic_id"],
        doctor_id=doctor_id,
        appointment_time=appointment_time,
        documents=documents,
        created_by=f"CLINIC_{current_clinic['clinic_id']}"
    )