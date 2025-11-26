from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from app.context_user import get_current_user
from app.repositories.activity_repository import ActivityRepository
from app.repositories.deal_repository import DealRepository
from app.schemas.activity_schemas import ActivityCreateSchema
from app.schemas.paginate_schema import PaginationGetActivities, ActivitiesPage, PageMeta
from app.services.base_services import BaseServices
from app.utils.raises import _not_found


class ActivityService(BaseServices):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo_active = ActivityRepository(self.session)
        self.repo_deal = DealRepository(self.session)

    async def create_activity_route(self, deal_id: int, activ_data: ActivityCreateSchema):
        deal = await self.repo_deal.get_deal(deal_id=deal_id, org_id=get_current_user().org_id)
        if deal is None:
            raise _not_found("Not found deal")
        # Соответственно комментирвоать сделку могут только высшие сотрудники организации лиюбо хозяева сделки
        await self.access_utils.check_create_activity_access(deal.user_id, self.valid_roles)
        result_active = await self.repo_active.create_activity(deal_id, get_current_user().id, activ_data.type, activ_data.payload)
        await self.repo_active.session.commit()
        return result_active

    async def get_list_activities_deal(self, deal_id: int, pag_data: PaginationGetActivities):
        deal = await self.repo_deal.get_deal(deal_id=deal_id, org_id=get_current_user().org_id)
        # Смотрим есть ли такая сделка внутри огранизации вообще
        if deal is None:
            raise _not_found("Not found deal")
        # Соответственно смотрим вобще имеем ли мы право смотреть данные по сделке
        await self.access_utils.check_get_list_activity_access(deal.user_id, self.valid_roles)
        activ, total = await self.repo_active.get_list_activities(deal_id, pag_data)
        pages = ceil(total / pag_data.page_size) if pag_data.page_size else 1
        return ActivitiesPage(
            meta=PageMeta(total=total, limit=pag_data.page_size, pages=pages),
            activities=activ,
        )

