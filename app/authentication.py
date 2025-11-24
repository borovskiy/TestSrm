from typing import List, Optional, Annotated
from fastapi import Depends, Header, HTTPException, status, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.context_user import set_current_user
from app.dependencies import organization_services
from app.services.organisation_service import OrganizationService
from app.utils.auth_utils import AuthUtils
from app.utils.raises import _not_found

auth_scheme = HTTPBearer(auto_error=False)






# --- Dependencies ---
def get_token(credentials: Optional[HTTPAuthorizationCredentials] = Security(auth_scheme)) -> str:
    """
    Извлекает токен из Authorization header, выбрасывает 401 если нет.
    """
    if not credentials or not credentials.scheme.lower() == "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
    return credentials.credentials


def require_roles(
        allowed_roles: List[str] = None,
):
    async def dependency(
            organization_serv: Annotated[OrganizationService, Depends(organization_services)],
            token: str = Depends(get_token),  # твоя функция получения токена
            x_organization_id: Optional[int] = Header(None, alias="X-Organization-Id"),

    ):
        # Валидация токен сразу до основной логики
        user_payload = AuthUtils.verify_token(token)  # твоя функция валидации

        # Если треуются роли значит нужна организация, но если заголовка нет - ошибка
        if allowed_roles and not None and x_organization_id is None:
            raise _not_found("X-Organization-Id required")

        # Если все же есть organization_id - получаем данные организации
        if x_organization_id:
            organization_data = await organization_serv.get_user_organisations(user_id=user_payload.id, ogr_id=x_organization_id)
            if organization_data is None:
                raise _not_found("Not found user organisation")
            user_payload.org_id = x_organization_id
            user_payload.role_in_organization = organization_data.role.value

            # Проверяем роли если установлены
            user_roles = []
            if user_payload.role_in_organization:
                user_roles.append(user_payload.role_in_organization)

            if not any(role in allowed_roles for role in user_roles):
                raise HTTPException(403, "Insufficient permissions")
        set_current_user(user_payload)
    return dependency
