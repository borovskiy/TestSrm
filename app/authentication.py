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


async def _no_roles_dependency(
    token: str = Depends(get_token),
):
    user_payload = AuthUtils.verify_token(token)
    set_current_user(user_payload)


def _roles_dependency_factory(allowed_roles: List[str]):
    async def _roles_dependency(
        organization_serv: Annotated[OrganizationService, Depends(organization_services)],
        token: str = Depends(get_token),
        x_organization_id: int = Header(alias="X-Organization-Id"),
    ):
        user_payload = AuthUtils.verify_token(token)
        org_data = await organization_serv.get_user_organisations(
            user_id=user_payload.id,
            ogr_id=x_organization_id
        )
        if org_data is None:
            raise _not_found("User not registered in organisation")
        user_payload.org_id = x_organization_id
        user_payload.role_in_organization = org_data.role.value
        if user_payload.role_in_organization not in allowed_roles:
            raise HTTPException(403, "Insufficient permissions")
        set_current_user(user_payload)
    return _roles_dependency

def require_roles(allowed_roles: Optional[List[str]] = None):
    if allowed_roles:
        return _roles_dependency_factory(allowed_roles)
    return _no_roles_dependency