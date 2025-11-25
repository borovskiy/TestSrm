from math import ceil
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.context_user import get_current_user
from app.models.deal import DealStatus, DealStage
from app.repositories.contact_repository import ContactRepository
from app.repositories.deal_repository import DealRepository
from app.schemas.deal_schemas import DealCreateSchema, DealCreateSchemaFull, DealPatchSchema, DealFilterSchema, \
    DealListResponseSchema
from app.services.base_services import BaseServices
from app.utils.raises import _forbidden


class DealService(BaseServices):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo_deal = DealRepository(self.session)
        self.repo_contact = ContactRepository(self.session)

    async def list_deals(self, status: List[DealStatus], stage: List[DealStage], filters: DealFilterSchema):
        if filters.user_id is not None:
            self.access_utils.check_get_list_deal_access(filters.user_id, self.valid_roles)
        deals, total = await self.repo_deal.list_deal_filtered(get_current_user().org_id, status, stage, filters)
        pages = ceil(total / filters.page_size) if filters.page_size else 1
        result = DealListResponseSchema(deals=deals, total=total, pages=pages,page=filters.page_size, page_size=filters.page_size)
        return result

    async def create_deal(self, user_id: int, data_deal: DealCreateSchema):
        self.log.info(f"create_deal")
        # проверяем доступы для создания сделки
        self.access_utils.check_create_deal_access(user_id, self.valid_roles)
        new_deal_data = DealCreateSchemaFull(**data_deal.model_dump())
        new_deal_data.organization_id = get_current_user().org_id
        # ЗАкрепляем сделку за организацией
        result = await self.repo_deal.create_one_obj_model(new_deal_data.model_dump())
        await self.repo_deal.session.commit()
        return result

    async def update_status_deal(self, user_id: int, deal_id: int, data_deal: DealPatchSchema):
        self.log.info(f"update_status_deal")
        # проверяем доступы для обновления статусов сделки
        self.access_utils.check_update_deal_access(user_id, deal_id, self.valid_roles)

        curr_user = get_current_user()
        org_id = curr_user.org_id
        deal = await self.repo_deal.get_deal(deal_id, org_id)
        if data_deal.status == DealStatus.WON and deal.amount <= 0:
            self.log.warning("deal amount must not be negative or zero")
            raise _forbidden("deal amount must not be negative or zero")
        if not DealStatus.rollback_validation(data_deal.status.value, curr_user.role_in_organization,
                                              deal.status.value):
            self.log.warning("deal amount must not be negative or zero")
            raise _forbidden("deal amount must not be negative or zero")
        result = await self.repo_deal.update_model_id(deal_id, data_deal.model_dump())
        return result

    async def remove_deal(self, user_id: int, deal_id: int):
        self.log.info(f"update_status_deal")
        self.access_utils.check_remove_deal_access(user_id, deal_id, self.valid_roles)

        return await self.repo_deal.delete_by_id(deal_id)
