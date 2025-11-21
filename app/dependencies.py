from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.services.auth_service import AuthService
from app.services.contact_service import ContactService
from app.services.organisation_service import OrganizationService
from app.settings import settings

SessionLocal = async_sessionmaker(
    bind=create_async_engine(settings.DATABASE_URL, echo=False, ),
    expire_on_commit=False,
)


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


def auth_services(session: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(session)


def organization_services(session: AsyncSession = Depends(get_db)) -> OrganizationService:
    return OrganizationService(session)


def contact_services(session: AsyncSession = Depends(get_db)) -> ContactService:
    return ContactService(session)
