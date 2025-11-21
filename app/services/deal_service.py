from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base_services import BaseServices


class DealService(BaseServices):
    def __init__(self, session: AsyncSession):
        super().__init__()
        # self.repo_user = UserRepository(session)
        # self.repo_org = OrganizationRepository(session)
        # self.repo_org_mem = OrganizationMemberRepository(session)