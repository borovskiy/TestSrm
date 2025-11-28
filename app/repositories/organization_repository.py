from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models import OrganizationModel, OrganizationMemberModel
from app.repositories.base_repository import BaseRepo
from app.schemas.paginate_schema import PaginationOrgGet


class OrganizationRepository(BaseRepo[OrganizationModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OrganizationModel)
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

    async def get_list_organisation_for_user(
        self,
        user_id: int,
        pagination: PaginationOrgGet
    ):
        self.log.info("get_list_organisation_for_user")
        base_stmt = (
            select(self.org_mem_model)
            .join(self.org_mem_model.organization)
            .where(self.org_mem_model.user_id == user_id)
        )

        if pagination.search:
            base_stmt = base_stmt.where(
                self.org_mem_model.organization.has(
                    OrganizationModel.name.ilike(f"%{pagination.search}%")
                )
            )
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total_res = await self.session.execute(count_stmt)
        total = total_res.scalar() or 0
        stmt_paginated = (
            base_stmt
            .options(joinedload(self.org_mem_model.organization))
            .offset(pagination.page * pagination.page_size)
            .limit(pagination.page_size)
        )

        data_res = await self.session.execute(stmt_paginated)
        organisation = data_res.scalars().all()
        return organisation, total

    async def get_organisation_by_name(self, name: str):
        self.log.info("get_organisation_by_name")
        stmt_exercise = (
            select(self.main_model)
            .where(self.main_model.name == name)
        )
        res = await self.session.execute(stmt_exercise)
        return res.scalars().first()
