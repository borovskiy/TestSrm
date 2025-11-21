from app.models.organization_member import RoleEnum
from app.schemas.base_schema import BaseModelSchema, BaseIdSchema


class OrganizationCreateSchema(BaseModelSchema):
    name: str


class OrganizationGetSchema(OrganizationCreateSchema, BaseIdSchema):
    ...


class OrganizationGetListSchema(BaseModelSchema):
    organization: OrganizationGetSchema
    role: RoleEnum
