from typing import Annotated

from fastapi import APIRouter, Depends

from app.authentication import require_roles
from app.context_user import get_current_user
from app.dependencies import deal_services
from app.models.organization_member import RoleEnum
from app.schemas.deal_schemas import DealCreateSchema, DealGetSchema, DealPatchSchema
from app.services.deal_service import DealService

router = APIRouter(
    prefix="/v1/deals",
    tags=["Deal"],
)


# @router.get("/list",
#             response_model=ContactsPage,
#             status_code=200,
#             dependencies=[Depends(require_roles(
#                 [RoleEnum.MEMBER.value, RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value, ]))]
#             )
# async def get_contacts(
#         contact_serv: Annotated[DealService, Depends(deal_services)],
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
#         contact_serv: Annotated[DealService, Depends(deal_services)],
#         contact_data: ContactsAddSchema,
# ):
#     ...


@router.post("/",
             response_model=DealGetSchema,
             status_code=201,
             dependencies=[Depends(require_roles(
                 [RoleEnum.MEMBER.value, RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value]))]
             )
async def add_deal(
        deal_serv: Annotated[DealService, Depends(deal_services)],
        deal_data: DealCreateSchema,
        user_id: int | None = None,
):
    """
    Создаем сделку для пользователя в конкретной огранизации
    OWNER, MANAGER, ADMIN могут назначить сделку на юзера в организации
    """
    return await deal_serv.create_deal(user_id or get_current_user().id, deal_data)


@router.patch("/{deal_id}",
              response_model=DealGetSchema,
              status_code=201,
              dependencies=[Depends(require_roles(
                  [RoleEnum.MEMBER.value, RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value]))]
              )
async def update_deal(
        deal_serv: Annotated[DealService, Depends(deal_services)],
        deal_data: DealPatchSchema,
        deal_id: int,
        user_id: int | None = None,
):
    """
    Изменяем данные по сделке
    OWNER, MANAGER, ADMIN могут менять сделку определенному юзеру в организации
    """
    return await deal_serv.update_status_deal(user_id or get_current_user().id, deal_id, deal_data)


@router.delete("/{deal_id}",
              response_model=DealGetSchema,
              status_code=201,
              dependencies=[Depends(require_roles(
                  [RoleEnum.MEMBER.value, RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value]))]
              )
async def update_deal(
        deal_serv: Annotated[DealService, Depends(deal_services)],
        deal_data: DealPatchSchema,
        deal_id: int,
        user_id: int | None = None,
):
    """
    Изменяем данные по сделке
    OWNER, MANAGER, ADMIN могут менять сделку определенному юзеру в организации
    """
    return await deal_serv.update_status_deal(user_id or get_current_user().id, deal_id, deal_data)