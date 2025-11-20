from contextvars import ContextVar
from typing import Optional

from app.logging_conf import request_user_var
from app.schemas.auth_schemas import UserSchemaPayload
from app.utils.raises import _unauthorized

_current_user: ContextVar[Optional[UserSchemaPayload]] = ContextVar("current_user", default=None)

def set_current_user(user: UserSchemaPayload) -> None:
    _current_user.set(user)
    try:
        val = None
        if hasattr(user, "email") and user.email:
            val = user.email
        elif hasattr(user, "id") and user.id is not None:
            val = f"id={user.id}"
        request_user_var.set(val or "-")
    except Exception:
        request_user_var.set("-")


def get_current_user() -> UserSchemaPayload:
    user = _current_user.get()
    if user is None:
        raise _unauthorized("No current user")
    return user