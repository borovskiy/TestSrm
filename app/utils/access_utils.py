from sqlalchemy.ext.asyncio import AsyncSession

from app.context_user import get_current_user
from app.repositories.contact_repository import ContactRepository
from app.repositories.deal_repository import DealRepository
from app.repositories.organization_members_repository import OrganizationMemberRepository
from app.utils.raises import _forbidden


class AccessUtils:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.cont_org_rep = ContactRepository(session)
        self.org_mem_rep = OrganizationMemberRepository(session)
        self.deal_rep = DealRepository(session)


    async def check_get_list_deal_access(self, target_user_id, valid_roles):
        await self.check_access_role(target_user_id, valid_roles)
        await self.check_access_user_org(target_user_id)

    async def check_create_deal_access(self, target_user_id, valid_roles):
        await self.check_access_role(target_user_id, valid_roles)
        await self.check_access_user_org(target_user_id)

    async def check_contact_access(self, target_user_id, valid_roles, update):
        await self.check_create_deal_access(target_user_id, valid_roles)
        await self.check_contact_org(target_user_id, update)

    async def check_remove_deal_access(self, target_user_id: int, deal_id: int, valid_roles: list):
        await self.check_update_deal_access(target_user_id, deal_id, valid_roles)

    async def check_update_deal_access(self, target_user_id: int, deal_id: int, valid_roles: list):
        await self.check_create_deal_access(target_user_id, valid_roles)
        await self.check_deal_exist_org(target_user_id, deal_id)

    @classmethod
    async def check_access_role(cls, target_user_id: int, valid_roles: list):
        if target_user_id != get_current_user().id and get_current_user().role_in_organization not in valid_roles:
            # Проверяем если ид юзера не свой собственный то должны быть права для создания или изменения
            raise _forbidden("You do not have the right to change contact data for the current user")

    async def check_access_user_org(self, target_user_id: int):
        if await self.org_mem_rep.get_member_in_organisation(org_id=get_current_user().org_id,
                                                             user_id=target_user_id) is None:
            # Смотрим есть ли такой юзер в организации вообще если нет - пошел вон
            raise _forbidden("You do not have the right to change contact data for the current user")

    async def check_contact_org(self, target_user_id: int, update: bool):
        contact_user_org = await self.cont_org_rep.get_contact_by_org(org_id=get_current_user().org_id,
                                                                      user_id_cont=target_user_id)
        if update:
            # Если мы запускаем обновление контакта
            if contact_user_org is None:
                # Если такого контакта нет то обновить нельзя
                raise _forbidden("You do not have the right to change contact data for the current user")
        else:
            # Если мы пытаемся создать новый окнтакт
            if contact_user_org is not None:
                # Если контакт уже был то то нельзя создать новый
                raise _forbidden("you already have a contact for this organization")

    async def check_deal_exist_org(self, target_user_id: int, deal_id: int):
        # Проверяем а вобще есть ли такая сделка у организации на юзере, если нет - пошел вон
        if await self.deal_rep.exist_deal_for_user_org(target_user_id, deal_id, get_current_user().org_id):
            raise _forbidden("Not found deal")
