from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.activity_repository import ActivityRepository
from app.services.base_services import BaseServices


class ActivityService(BaseServices):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.repo_user = ActivityRepository(session)
        # self.repo_org = OrganizationRepository(session)
        # self.repo_org_mem = OrganizationMemberRepository(session)