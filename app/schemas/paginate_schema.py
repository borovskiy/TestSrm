from typing import Sequence

from pydantic import Field

from app.schemas.base_schema import BaseModelSchema
from app.schemas.contact_schema import ContactsSchema


class PageMeta(BaseModelSchema):
    total: int
    limit: int
    pages: int

class PaginationGet(BaseModelSchema):
    page: int = Field(default=0, ge=0)
    page_size: int = Field(default=10, ge=1)
    search: str | None = None
    owner_id: int | None = None


class ContactsPage(BaseModelSchema):
    meta: PageMeta
    contacts: Sequence[ContactsSchema]