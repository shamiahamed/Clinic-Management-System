import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

# Load same config used in security.py
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# This tells Swagger where to look for the login token
# Use the full path to your login-by-id endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login-by-id")

async def get_current_clinic(token: str = Depends(oauth2_scheme)):
    """
    Dependency to validate the token and return clinic info.
    Ensures 'CLINIC' role and extracts 'clinic_id'.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "status": "error", 
            "message": "Could not validate credentials",
            "code": "AUTH_FAILED"
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 2. Extract specific data your mentor wants
        clinic_id: int = payload.get("clinic_id")
        username: str = payload.get("sub")
        role: str = payload.get("role")

        # 3. Validation Logic
        if clinic_id is None or username is None:
            raise credentials_exception
            
        # Mentor's requirement: Ensure user is a 'CLINIC' admin
        if role != "CLINIC":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "status": "error",
                    "message": "Access denied. Only Clinic administrators allowed."
                }
            )

        # 4. Return info for use in the controller/service
        return {
            "clinic_id": clinic_id,
            "username": username,
            "role": role
        }

    except JWTError:
        raise credentials_exception

# Helpful wrapper for different permission levels
def allow_roles(allowed_roles: list[str]):
    """If you ever need to allow STAFF or DOCTOR later"""
    async def role_checker(current_user: dict = Depends(get_current_clinic)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Role not permitted")
        return current_user
    return role_checker