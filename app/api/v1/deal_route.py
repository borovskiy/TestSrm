from typing import Annotated, List

from fastapi import APIRouter, Depends, Query

from app.core.authentication import require_roles
from app.core.context_user import get_current_user
from app.core.dependencies import deal_services
from app.models.deal import DealStatus, DealStage
from app.models.organization_member import RoleEnum
from app.schemas.deal_schemas import DealCreateSchema, DealGetSchema, DealPatchSchema, DealFilterSchema, \
    DealListResponseSchema
from app.services.deal_service import DealService

router = APIRouter(
    prefix="/v1/deals",
    tags=["Deals"],
)


@router.get("/list",
            response_model=DealListResponseSchema,
            status_code=200,
            dependencies=[Depends(require_roles(
                [RoleEnum.MEMBER.value, RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value]
            ))]
            )
async def list_deals(
        deal_serv: Annotated[DealService, Depends(deal_services)],
        status: List[DealStatus] = Query([]),
        stage: List[DealStage] = Query([]),
        filters: DealFilterSchema = Depends(DealFilterSchema),

):
    """
    Получаем список сделок с фильтрами
    """
    return await deal_serv.list_deals(status, stage,  filters)


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
async def update_status_deal(
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
async def delete_deal(
        deal_serv: Annotated[DealService, Depends(deal_services)],
        deal_data: DealPatchSchema,
        deal_id: int,
        user_id: int | None = None,
):
    """
    Изменяем данные по сделке
    OWNER, MANAGER, ADMIN могут менять сделку определенному юзеру в организации
    """
    return await deal_serv.remove_deal(user_id or get_current_user().id, deal_id, deal_data)
