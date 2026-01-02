from sqlalchemy.ext.asyncio import AsyncSession

from app.services.appointment_service import (
    create_appointment,
    get_all_appointments,
    get_appointment_by_id,
    get_appointments_by_doctor,
    update_appointment_status
)


class AppointmentController:

    @staticmethod
    async def create(db: AsyncSession, payload):
        return await create_appointment(db, payload)

    @staticmethod
    async def list(db: AsyncSession):
        return await get_all_appointments(db)

    @staticmethod
    async def get_by_id(db: AsyncSession, appointment_id: int):
        return await get_appointment_by_id(db, appointment_id)

    @staticmethod
    async def get_by_doctor(db: AsyncSession, doctor_id: int):
        return await get_appointments_by_doctor(db, doctor_id)

    @staticmethod
    async def update_status(
        db: AsyncSession,
        appointment_id: int,
        new_status,
        updated_by: str
    ):
        return await update_appointment_status(
            db=db,
            appointment_id=appointment_id,
            new_status=new_status,
            updated_by=updated_by
        )
