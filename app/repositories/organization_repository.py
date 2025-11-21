from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models import OrganizationModel, OrganizationMemberModel
from app.repositories.base_repository import BaseRepo


class OrganizationRepository(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.main_model = OrganizationModel
        self.org_mem_model = OrganizationMemberModel

    async def checking_existence_organization_by_name(self, name_org: str):
        # Если такая существует то тру
        self.log.info("get_find_organization_name %s ", name_org)
        stmt = select(self.main_model).where(self.main_model.name == name_org)
        return await self.execute_session_get_one(stmt)

    async def checking_existence_organization_by_id(self, org_id: int):
        # Если такая существует то тру
        self.log.info("checking_existence_organization_by_id")
        stmt = select(self.main_model).where(self.main_model.id == org_id)
        return await self.execute_session_get_one(stmt)

    async def get_list_organisation_for_user(self, user_id: int):
        self.log.info("get_list_obj")
        stmt_exercise = (

            select(self.org_mem_model)
            .options(joinedload(self.org_mem_model.organization))
            .where(self.org_mem_model.user_id==user_id)
        )
        res = await self.session.execute(stmt_exercise)
        return res.scalars().all()

    async def get_organisation_by_name(self, name: str):
        self.log.info("get_organisation_by_name")
        stmt_exercise = (
            select(self.main_model)
            .where(self.main_model.name == name)
        )
        res = await self.session.execute(stmt_exercise)
        return res.scalars().first()
