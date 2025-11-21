from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DealModel
from app.repositories.base_repository import BaseRepo
from app.utils.raises import _forbidden


class DealRepository(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.main_model = DealModel

    async def get_check_deal_for_request(self, deal_id: int, org_id) -> DealModel | None:
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
        object_response = res.scalars().first()
        if object_response is None:
            raise _forbidden("Not found deal")
        return object_response
