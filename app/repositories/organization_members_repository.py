from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import OrganizationMemberModel
from app.repositories.base_repository import BaseRepo
from app.models.organization_member import RoleEnum
from app.schemas.organisation_schemas import OrgRoleEnum


class OrganizationMemberRepository(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.main_model = OrganizationMemberModel

    async def add_members_in_organisation(self, org_id: int, user_id: int, role: OrgRoleEnum):
        # закрепляем юзера за организацией
        self.log.info(f"add_members_in_organisation")
        obj = OrganizationMemberModel(organization_id=org_id, user_id=user_id, role=role.name)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get_member_in_organisation(self, org_id: int, user_id: int) -> OrganizationMemberModel | None:
        # получаем юзера с организацией
        self.log.info(f"add_members_in_organisation")
        stmt = select(self.main_model).where(
            self.main_model.organization_id == org_id,
            self.main_model.user_id == user_id
        )
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def get_member_in_org_with_deal(self, org_id: int, user_id: int) -> OrganizationMemberModel | None:
        # получаем юзера с организацией
        self.log.info(f"add_members_in_organisation")
        stmt = (select(self.main_model)
        .options(joinedload(self.org_mem_model.organization))
        .where(
            self.main_model.organization_id == org_id,
            self.main_model.user_id == user_id
        ))
        res = await self.session.execute(stmt)
        return res.scalars().first()
