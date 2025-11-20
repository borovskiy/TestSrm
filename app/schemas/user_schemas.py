from app.schemas.base_schema import BaseModelSchema, BaseIdSchema


class UserPayloadToken(BaseModelSchema, BaseIdSchema):
    email: str
    name: str
