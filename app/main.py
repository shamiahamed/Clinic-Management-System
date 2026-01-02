from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.session import engine
from app.db.base import Base # This now includes all your models!

# Import routers
from app.routes.clinic_routes import router as clinic_router
from app.routes.doctor_routes import router as doctor_router
from app.routes.patient_routes import router as patient_router
from app.routes.appointment_routes import router as appointment_router
from app.routes.authentication_routes import router as authentication_router

#Import Middleware
from app.middleware.request_logging import RequestLoggingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")
    
    yield
    
    # SHUTDOWN
    await engine.dispose()
    print("Database connection closed.")


# CREATE APP ONLY ONCE
app = FastAPI(
    title="Clinic Management System",
    version="0.1.0",
    lifespan=lifespan,
    description="Enterprise API - Clinic System",
    swagger_ui_parameters={
        "tryItOutEnabled": True,
        "defaultModelsExpandDepth": -1
    },
    docs_url="/api-explorer/swagger" 
)

app.add_middleware(RequestLoggingMiddleware)

# Routers
app.include_router(authentication_router)
app.include_router(clinic_router)
app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(appointment_router)


#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJUZW5zYXciLCJjbGluaWNfaWQiOjksInJvbGUiOiJDTElOSUMiLCJleHAiOjE3NjcwNzkwMTZ9.Mpmgc4Pl0wK5b1ckre6SujH3EO8eSSyFLui6IXwbnvg
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJHYWxheHkiLCJjbGluaWNfaWQiOjEwLCJyb2xlIjoiQ0xJTklDIiwiZXhwIjoxNzY3MDg1NTEwfQ.9wLgnmj3qZvZFxSFE96KGgnMK6rnzBs1FsKl5dFX_B0