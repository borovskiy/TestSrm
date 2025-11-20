from app.schemas.base_schema import BaseModelSchema, BaseIdSchema


class OrganizationCreateSchema(BaseModelSchema):
    name: str

class OrganizationGetListSchema(OrganizationCreateSchema, BaseIdSchema):
    ...