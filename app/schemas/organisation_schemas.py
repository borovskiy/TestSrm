from enum import Enum
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


class OrgRoleEnum(str, Enum):
    OWNER = RoleEnum.OWNER.value
    MANAGER = RoleEnum.MANAGER.value
    MEMBER = RoleEnum.MEMBER.value

class OrganizationAddUserSchema(BaseModelSchema):
    user_id: int
    role: OrgRoleEnum

class OrganizationRemoveUserSchema(BaseModelSchema):
    user_id: int