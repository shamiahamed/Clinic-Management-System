from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.controllers.clinic_controller import ClinicController
from app.schemas.clinic_schema import ClinicCreate,ClinicResponse

router = APIRouter(prefix="/clinic", tags=["Clinic"])

@router.post("",response_model=ClinicResponse)
async def create_clinic(
    payload: ClinicCreate,
    db: AsyncSession = Depends(get_db)
):
    
    return await ClinicController.create(
        db=db,
        payload=payload,
        created_by="admin"
    )