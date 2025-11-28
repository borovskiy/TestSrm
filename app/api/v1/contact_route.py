import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.authentication import require_roles
from app.core.context_user import get_current_user
from app.core.dependencies import contact_services
from app.models.organization_member import RoleEnum
from app.schemas.contact_schema import ContactsAddSchema, ContactsSchema
from app.schemas.paginate_schema import ContactsPage, PaginationGetCont
from app.services.contact_service import ContactService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/v1/contacts",
    tags=["Contacts"],
)
## Роут для работы с контактными данными

@router.get("/list",
            response_model=ContactsPage,
            status_code=200,
            dependencies=[Depends(require_roles(
                [RoleEnum.MEMBER.value, RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value, ]))]
            )
async def get_contacts(
        contact_serv: Annotated[ContactService, Depends(contact_services)],
        pagination: PaginationGetCont = Depends(PaginationGetCont),
):
    """
    Получаем все контакты в текущей организации
    Так же можно искать контакт по id юзера или по контакным данным
    """
    return await contact_serv.get_contacts_org(pagination)


@router.post("/",
             response_model=ContactsSchema,
             status_code=201,
             dependencies=[Depends(require_roles(
                 [RoleEnum.MEMBER.value, RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value]))]
             )
async def add_contact(
        contact_serv: Annotated[ContactService, Depends(contact_services)],
        contact_data: ContactsAddSchema,
        user_id: int | None = None,

):
    """
    Добавляем контакт для юзера в органиации
    Участник member может добавить только свой контакт в определенной огранизации
    """
    return await contact_serv.add_contact(user_id or get_current_user().id, contact_data)


@router.put("/",
            response_model=ContactsSchema,
            status_code=200,
            dependencies=[Depends(require_roles(
                [RoleEnum.MEMBER.value, RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value, ]))]
            )
async def update_contact(
        contact_serv: Annotated[ContactService, Depends(contact_services)],
        contact_data: ContactsAddSchema,
        user_id: int | None = None,
):
    """
    Обновляем контакт для юзера в органиации
    Участник member может обновить только свой контакт в определенной огранизации
    """
    ##
    return await contact_serv.update_contact(user_id or get_current_user().id, contact_data)