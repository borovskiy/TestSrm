from app.schemas.base_schema import BaseModelSchema


class ContactsSchema(BaseModelSchema):
    owner_id: int
    name: str
    email: str
    phone: str
    id: int

class ContactsAddSchema(BaseModelSchema):
    name: str
    email: str
    phone: str

