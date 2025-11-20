from pydantic import BaseModel, EmailStr, Field

from app.schemas.base_schema import BaseModelSchema


class UserRegisterSchemaReq(BaseModelSchema):
    email: EmailStr | None = Field(default=None)
    hashed_password: str = Field(..., min_length=8)
    name: str
    organization_name: str


class UserRegisterSchemaCreatedRes(BaseModel):
    email: EmailStr | None = Field(default=None)
    hashed_password: str = Field(..., min_length=8)
    name: str


class LoginUserReq(BaseModel):
    email: str
    password: str


class UserSchemaPayload(BaseModelSchema):
    id:int
    email: str
    name: str
    organization_id: int | None = None
    role_in_organization: str | None = None

    exp: int | None = None

class TokenAccessRes(BaseModel):
    access_token: str

class TokenRefreshRes(BaseModel):
    refresh_token: str

class TokenFullRes(TokenAccessRes, TokenRefreshRes):
    ...



class PayloadToken(BaseModel):
    token_limit_verify: int
    time_now: int
    user_id: int
    type: str
