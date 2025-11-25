from typing import List, Any, Coroutine, Sequence

from sqlalchemy import select, and_, func, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DealModel
from app.models.deal import DealStatus, DealStage
from app.repositories.base_repository import BaseRepo
from app.schemas.deal_schemas import DealFilterSchema, OrderEnum


class DealRepository(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.main_model = DealModel

    async def get_deal(self, deal_id: int, org_id) -> DealModel | None:
        self.log.info(f"get_check_deal_for_request")
        stmt = (
            select(self.main_model)
            .where(
                and_(
                    self.main_model.organization_id == org_id,
                    self.main_model.id == deal_id
                )

            ))
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def list_deal_filtered(
            self,
            org_id: int,
            status: List[DealStatus],
            stage: List[DealStage],
            filters: DealFilterSchema
    ) -> tuple[Sequence[Row[Any] | RowMapping | Any], Any | None]:
        base_stmt = select(self.main_model).where(self.main_model.organization_id == org_id)
        base_stmt = self._apply_filters(base_stmt, status, stage, filters, self.main_model)

        count_stmt = select(func.count()).select_from(self.main_model)
        count_stmt = self._apply_filters(count_stmt, status, stage, filters, self.main_model)

        # ordering + pagination
        order_column = getattr(self.main_model, filters.order_by.value)
        paged_stmt = base_stmt.order_by(
            order_column.desc() if filters.order == OrderEnum.desc else order_column.asc()
        ).offset((filters.page - 1) * filters.page_size).limit(filters.page_size)

        # execute
        deals = (await self.session.execute(paged_stmt)).scalars().all()
        total = await self.session.scalar(count_stmt)

        return deals, total

    def _apply_filters(self, stmt, status, stage, filters, model):
        if status:
            stmt = stmt.where(model.status.in_([s.name for s in status]))
        if stage:
            stmt = stmt.where(model.stage.in_([s.name for s in stage]))
        if filters.min_amount is not None:
            stmt = stmt.where(model.amount >= filters.min_amount)
        if filters.max_amount is not None:
            stmt = stmt.where(model.amount <= filters.max_amount)
        if filters.user_id is not None:
            stmt = stmt.where(model.user_id == filters.user_id)
        return stmt

    async def exist_deal_for_user_org(self, user_id: int, deal_id: int, ord_id: int) -> bool:
        self.log.info(f"exist_deal_user")
        stmt = (
            select(self.main_model)
            .where(
                and_(
                    self.main_model.organization_id == ord_id,
                    self.main_model.id == deal_id,
                    self.main_model.user_id == user_id
                )

            ))
        res = await self.session.execute(stmt)
        if res.scalars().first() is None:
            return True
        return False
