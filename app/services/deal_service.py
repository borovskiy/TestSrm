from sqlalchemy.ext.asyncio import AsyncSession

from app.context_user import get_current_user
from app.models.deal import DealStatus
from app.repositories.contact_repository import ContactRepository
from app.repositories.deal_repository import DealRepository
from app.schemas.deal_schemas import DealCreateSchema, DealCreateSchemaFull, DealPatchSchema
from app.services.base_services import BaseServices
from app.utils.raises import _forbidden, _bad_request


class DealService(BaseServices):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.repo_deal = DealRepository(session)
        self.repo_contact = ContactRepository(session)

    async def create_deal(self, data_deal: DealCreateSchema):
        curr_user = get_current_user()
        org_id = curr_user.org_id

        contact_data = await self.repo_contact.get_check_contact_for_request(id_org=org_id, id_con=data_deal.contact_id, list_valid_roles=self.valid_roles)
        new_deal_data = DealCreateSchemaFull(**data_deal.model_dump())
        new_deal_data.owner_id = contact_data.owner_id
        new_deal_data.organization_id = org_id
        result = await self.repo_deal.create_one_obj_model(new_deal_data.model_dump())
        await self.repo_deal.session.commit()
        return result

    async def update_deal(self, deal_id: int, data_deal: DealPatchSchema):
        curr_user = get_current_user()
        org_id = curr_user.org_id
        deal = await self.repo_deal.get_check_deal_for_request(deal_id, org_id)
        await self.repo_contact.get_check_contact_for_request(id_org=org_id, id_con=deal.contact_id, list_valid_roles=self.valid_roles)
        if data_deal.status == DealStatus.WON and deal.amount <= 0:
            raise _bad_request()
        if not DealStatus.rollback_validation(data_deal.status.value, curr_user.role_in_organization, deal.status.value):
            raise _forbidden("You now downgrade status")
        result = await self.repo_deal.update_model_id(deal_id, data_deal.model_dump())
        return result