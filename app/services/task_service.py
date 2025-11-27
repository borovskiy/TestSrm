from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from app.context_user import get_current_user
from app.repositories.deal_repository import DealRepository
from app.repositories.tast_repository import TaskRepository
from app.schemas.paginate_schema import PaginationTasksWithDueGet, TasksPage, PageMeta
from app.schemas.task_schemas import TaskCreateRouteSchema, TaskCreateRouteFullSchema
from app.services.base_services import BaseServices
from app.utils.raises import _not_found


class TaskService(BaseServices):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo_task = TaskRepository(self.session)
        self.repo_deal = DealRepository(self.session)

    async def create_tasks(self, data: TaskCreateRouteSchema, deal_id: int):
        deal = await self.access_utils.check_deal_for_org(deal_id=deal_id, org_id=get_current_user().org_id)
        # Тут понятно
        await self.access_utils.check_access_role(deal.user_id, self.valid_roles)
        update_data = TaskCreateRouteFullSchema(**data.model_dump())
        update_data.deal_id = deal_id
        result = await self.repo_task.create_one_obj_model(update_data.model_dump())
        await self.session.commit()
        return result

    async def get_tasks_for_deals(self, pag: PaginationTasksWithDueGet):
        deal = await self.access_utils.check_deal_for_org(deal_id=pag.deal_id, org_id=get_current_user().org_id)
        await self.access_utils.check_access_role(deal.user_id, self.valid_roles)

        tasks, total = await self.repo_task.get_tasks_for_deals(pag_data=pag)
        pages = ceil(total / pag.page_size) if pag.page_size else 1

        return TasksPage(
            meta=PageMeta(total=total, limit=pag.page_size, pages=pages),
            contacts=tasks,
        )
