from typing import Annotated

from fastapi import APIRouter, Depends

from app.authentication import require_roles
from app.dependencies import activity_services
from app.models.organization_member import RoleEnum
from app.schemas.activity_schemas import ActivityCreateSchema, ActivityResponseSchema
from app.schemas.paginate_schema import PaginationGetActivities, ActivitiesPage
from app.services.activity_service import ActivityService

router = APIRouter(
    prefix="/v1",
    tags=["Activity"],
)


@router.post("/deals/{deal_id}/activities",
             response_model=ActivityResponseSchema,
             status_code=201,
             dependencies=[Depends(require_roles(
                 [RoleEnum.MEMBER.value, RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value]))]
             )
async def add_activity(
        deal_id: int,
        activ_serv: Annotated[ActivityService, Depends(activity_services)],
        activ_data: ActivityCreateSchema,
):
    """
    Создаем активность типа коммент для сделаок
    """
    return await activ_serv.create_activity_route(deal_id, activ_data)


@router.get("/deals/{deal_id}/activities",
            response_model=ActivitiesPage,
            status_code=201,
            dependencies=[Depends(require_roles(
                [RoleEnum.MEMBER.value, RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value]))]
            )
async def get_list_activity(
        activ_serv: Annotated[ActivityService, Depends(activity_services)],
        deal_id: int,
        pag_data: PaginationGetActivities = Depends(PaginationGetActivities),

):
    """
    Порлучаем список активностей для сделки
    """
    return await activ_serv.get_list_activities_deal(deal_id, pag_data)
