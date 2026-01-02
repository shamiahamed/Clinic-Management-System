from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # Added this
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models.clinic_model import Clinic 
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login-by-id")
async def login_by_clinic_id(
    # OAuth2PasswordRequestForm reads from the Swagger popup fields
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    # 1. Get the clinic_id from the 'username' field in the popup
    try:
        clinic_id = int(form_data.username)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please enter a numeric Clinic ID in the 'username' field."
        )

    # 2. Look up the clinic
    result = await db.execute(
        select(Clinic).where(Clinic.clinic_id == clinic_id)
    )
    clinic = result.scalar_one_or_none()

    if not clinic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clinic with ID {clinic_id} not found."
        )

    # 3. Generate Token
    access_token = create_access_token(
        data={
            "sub": clinic.clinic_name,
            "clinic_id": clinic.clinic_id, 
            "role": "CLINIC"
        }
    )

    # Standard OAuth2 response format
    return {
        "status": "success",
        "message": f"Welcome back, {clinic.clinic_name}",
        "access_token": access_token, 
        "token_type": "bearer"
    }