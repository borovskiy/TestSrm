from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.tast_repository import TaskRepository
from app.services.base_services import BaseServices


class TaskService(BaseServices):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.repo_user = TaskRepository(session)
        # self.repo_org = OrganizationRepository(session)
        # self.repo_org_mem = OrganizationMemberRepository(session)