from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TaskModel
from app.repositories.base_repository import BaseRepo
from app.schemas.paginate_schema import PaginationTasksWithDueGet


class TaskRepository(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.main_model = TaskModel

    async def get_tasks_for_deals(self, pag_data: PaginationTasksWithDueGet):
        page = pag_data.page
        page_size = pag_data.page_size

        stmt = select(self.main_model).where(
            self.main_model.deal_id == pag_data.deal_id
        )

        # ----- Фильтр: только открытые -----
        if pag_data.only_open:
            stmt = stmt.where(self.main_model.is_done.is_(False))

        if pag_data.due_before:
            stmt = stmt.where(self.main_model.due_date <= pag_data.due_before)

        # ----- Фильтр: due_after -----
        if pag_data.due_after:
            stmt = stmt.where(self.main_model.due_date >= pag_data.due_after)

        # ----- COUNT -----
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.session.execute(count_stmt)).scalar() or 0

        # ----- Pagination -----
        stmt_paginated = (
            stmt.order_by(self.main_model.id.desc())
            .offset(page * page_size)
            .limit(page_size)
        )

        result = await self.session.execute(stmt_paginated)
        rows = result.scalars().all()

        return rows, total
