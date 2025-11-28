from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ActivityModel
from app.models.activity import TypeActivity
from app.repositories.base_repository import BaseRepo
from app.schemas.paginate_schema import PaginationGetActivities


class ActivityRepository(BaseRepo[ActivityModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ActivityModel)
        self.main_model = ActivityModel

    async def create_activity(self, deal_id: int, author_id: int, type_activity: TypeActivity,
                              payload: dict) -> ActivityModel:
        activity = ActivityModel(
            deal_id=deal_id,
            author_id=author_id,
            type=TypeActivity[type_activity],
            payload=payload
        )

        self.session.add(activity)
        await self.session.flush()
        return activity

    async def get_list_activities(self, deal_id: int, pag_data: PaginationGetActivities):
        page = pag_data.page
        page_size = pag_data.page_size

        base_stmt = (
            select(self.main_model)
            .where(self.main_model.deal_id == deal_id)
        )

        # ---- COUNT ----
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total_res = await self.session.execute(count_stmt)
        total = total_res.scalar() or 0

        # ---- PAGINATED QUERY ----
        stmt_paginated = (
            base_stmt
            .order_by(self.main_model.id.desc())  # или created_at если есть
            .offset(page * page_size)
            .limit(page_size)
        )

        result = await self.session.execute(stmt_paginated)
        activ = result.scalars().all()

        return activ, total
