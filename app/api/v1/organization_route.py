import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.authentication import require_roles
from app.context_user import get_current_user
from app.dependencies import organization_services
from app.schemas.auth_schemas import UserSchemaPayload
from app.schemas.organisation_schemas import OrganizationCreateSchema, OrganizationGetListSchema
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


@router.post("/", response_model=OrganizationCreateSchema, status_code=201)
async def crete_organization(
        create_organization: OrganizationCreateSchema,
        organization_serv: Annotated[OrganizationService, Depends(organization_services)],
):
    """
    Создаем организацию
    """
    logger.info("Try create organisation")
    return await organization_serv.create_organization(create_organization)


@router.put("/{id_organization}", response_model=OrganizationCreateSchema, status_code=200)
async def update_name_organization(
        id_organization: int,
        register_organization: OrganizationCreateSchema,
        organization_serv: Annotated[OrganizationService, Depends(organization_services)],
):
    """
    Меняем имя организации
    """
    logger.info("Try update organisation")
    return await organization_serv.update_name_organization(id_organization, register_organization)
