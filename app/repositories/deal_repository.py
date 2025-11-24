from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DealModel
from app.repositories.base_repository import BaseRepo
from app.utils.raises import _forbidden


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
