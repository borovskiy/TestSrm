from typing import Annotated

from fastapi import APIRouter, Depends

from app.authentication import require_roles
from app.models.organization_member import RoleEnum

router = APIRouter(
    prefix="/v1/tasks",
    tags=["Task"],
)
# @router.get("/list",
#             response_model=ContactsPage,
#             status_code=200,
#             dependencies=[Depends(require_roles(
#                 [RoleEnum.MEMBER.value, RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value, ]))]
#             )
# async def get_contacts(
#         contact_serv: Annotated[ContactService, Depends(contact_services)],
#         pagination: PaginationGet = Depends(PaginationGet),
# ):
#     ...
#
#
# @router.put("/{id_contact}",
#             response_model=ContactsSchema,
#             status_code=200,
#             dependencies=[Depends(require_roles(
#                 [RoleEnum.MEMBER.value, RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value, ]))]
#             )
# async def update_contact(
#         id_contact: int,
#         contact_serv: Annotated[ContactService, Depends(contact_services)],
#         contact_data: ContactsAddSchema,
# ):
#     ...
#
#

