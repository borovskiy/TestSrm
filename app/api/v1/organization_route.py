import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.authentication import require_roles
from app.context_user import get_current_user
from app.dependencies import organization_services
from app.models.organization_member import RoleEnum
from app.schemas.organisation_schemas import OrganizationCreateSchema, OrganizationGetListSchema, OrganizationGetSchema
from app.services.organisation_service import OrganizationService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/v1/organisation",
    tags=["Organization"],
)


@router.get("/me",
            response_model=List[OrganizationGetListSchema],
            status_code=200,
            dependencies=[Depends(require_roles())]
            )
async def get_list_organization(
        organization_serv: Annotated[OrganizationService, Depends(organization_services)],
):
    """
    Получаем список организаций у пользователя
    """
    logger.info("Try get list organisation")
    print(get_current_user())
    return await organization_serv.get_list_organisations()


@router.post("/",
             response_model=OrganizationGetSchema,
             status_code=201,
             dependencies=[Depends(require_roles([RoleEnum.ADMIN.value]))])
async def crete_organization(
        create_organization: OrganizationCreateSchema,
        organization_serv: Annotated[OrganizationService, Depends(organization_services)],
):
    """
    Создаем организацию
    надо подумать кто вобще может их создавать
    """
    logger.info("Try create organisation")
    return await organization_serv.create_organization(create_organization)


@router.put("/",
            response_model=OrganizationGetSchema,
            status_code=200,
            dependencies=[Depends(require_roles([RoleEnum.ADMIN.value]))]
            )
async def update_name_organization(
        register_organization: OrganizationCreateSchema,
        organization_serv: Annotated[OrganizationService, Depends(organization_services)],
):
    """
    Меняем имя организации
    """
    logger.info("Try update organisation")
    return await organization_serv.update_name_organization(register_organization)
