import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.authentication import require_roles
from app.core.dependencies import organization_services
from app.models.organization_member import RoleEnum
from app.schemas.organisation_schemas import OrganizationCreateSchema, OrganizationGetSchema, OrganizationAddUserSchema, \
    OrganizationRemoveUserSchema
from app.schemas.paginate_schema import OrganisationPage, PaginationOrgGet
from app.services.organisation_service import OrganizationService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/v1/organisation",
    tags=["Organization"],
)


@router.get("/me",
            response_model=OrganisationPage,
            status_code=200,
            dependencies=[Depends(require_roles())]
            )
async def get_list_organization(
        organization_serv: Annotated[OrganizationService, Depends(organization_services)],
        pagination: PaginationOrgGet = Depends(PaginationOrgGet),
):
    """
    Получаем список организаций у пользователя
    """
    logger.info("Try get list organisation")
    return await organization_serv.get_list_organisations(pagination)


@router.put("/",
            response_model=OrganizationGetSchema,
            status_code=200,
            dependencies=[Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.OWNER.value]))]
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


@router.post("/",
             status_code=200,
             dependencies=[Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.OWNER.value]))])
async def add_member(
        create_organization: OrganizationAddUserSchema,
        organization_serv: Annotated[OrganizationService, Depends(organization_services)],
):
    """
    Добавляем участника в организацию
    """
    logger.info("add_member")
    return await organization_serv.add_member_in_organisation(create_organization)


@router.delete("/",
               status_code=200,
               dependencies=[Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.OWNER.value]))])
async def remove_member(
        data: OrganizationRemoveUserSchema,
        organization_serv: Annotated[OrganizationService, Depends(organization_services)],
):
    """
    Удаление участника из организации
    """
    logger.info("remove_member")
    return await organization_serv.remove_member_from_organisation(data)
