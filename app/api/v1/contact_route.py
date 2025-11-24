import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from app.authentication import require_roles
from app.dependencies import contact_services
from app.models import ContactModel
from app.models.organization_member import RoleEnum
from app.schemas.contact_schema import ContactsAddSchema, ContactsSchema
from app.schemas.paginate_schema import PaginationGet, ContactsPage
from app.services.contact_service import ContactService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/v1/contacts",
    tags=["Contacts"],
)


@router.get("/list",
            response_model=ContactsPage,
            status_code=200,
            dependencies=[Depends(require_roles(
                [RoleEnum.MEMBER.value, RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value, ]))]
            )
async def get_contacts(
        contact_serv: Annotated[ContactService, Depends(contact_services)],
        pagination: PaginationGet = Depends(PaginationGet),
):
    return await contact_serv.get_contact(pagination)


@router.put("/{id_contact}",
            response_model=ContactsSchema,
            status_code=200,
            dependencies=[Depends(require_roles(
                [RoleEnum.MEMBER.value, RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value, ]))]
            )
async def update_contact(
        id_contact: int,
        contact_serv: Annotated[ContactService, Depends(contact_services)],
        contact_data: ContactsAddSchema,
):
    return await contact_serv.update_contact(id_contact, contact_data)


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
    return await contact_serv.add_contact(user_id, contact_data)


@router.delete("/{contact_id}",
             response_model=ContactsSchema,
             status_code=200,
             dependencies=[Depends(require_roles(
                 [RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value]))]
             )
async def delete_contact(
        contact_serv: Annotated[ContactService, Depends(contact_services)],
        contact_data: ContactsAddSchema,
        user_id: int | None = None,
):
    return await contact_serv.delete_contact(user_id, contact_data)