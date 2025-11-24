from typing import Literal

from app.models.organization_member import RoleEnum
from app.schemas.base_schema import BaseModelSchema, BaseIdSchema


class OrganizationCreateSchema(BaseModelSchema):
    name: str


class OrganizationGetSchema(OrganizationCreateSchema, BaseIdSchema):
    ...


class OrganizationGetListSchema(BaseModelSchema):
    organization: OrganizationGetSchema
    role: RoleEnum


class OrganizationAddUserSchema(BaseModelSchema):
    user_id: int
    role: Literal[RoleEnum.OWNER, RoleEnum.MANAGER, RoleEnum.MEMBER]
