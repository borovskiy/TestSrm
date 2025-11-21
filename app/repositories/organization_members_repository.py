from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import OrganizationMemberModel
from app.repositories.base_repository import BaseRepo
from app.models.organization_member import RoleEnum


class OrganizationMemberRepository(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.main_model = OrganizationMemberModel

    async def add_members_in_organisation(self, organization_id: int, user_id: int):
        # закрепляем юзера за организацией
        self.log.info(f"add_members_in_organisation")
        obj = OrganizationMemberModel(organization_id=organization_id, user_id=user_id, role=RoleEnum.MEMBER)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get_members_in_organisation(self, organization_id: int, user_id: int) -> OrganizationMemberModel | None:
        # получаем юзера с организацией
        self.log.info(f"add_members_in_organisation")
        stmt = select(self.main_model).where(
            self.main_model.organization_id == organization_id,
            self.main_model.user_id == user_id
        )
        res = await self.session.execute(stmt)
        return res.scalars().first()
