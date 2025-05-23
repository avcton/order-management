from fastapi import HTTPException
from app.validators.auth import AccessTokenData


def has_privilege(user_data: AccessTokenData, privilege: str) -> bool:
    if privilege in user_data['privileges']:
        return

    raise HTTPException(
        status_code=403,
        detail=f"User does not have the required privileges"
    )


def has_any_privilege(user_data: AccessTokenData, privileges: list[str]) -> bool:
    if any(privilege in user_data['privileges'] for privilege in privileges):
        return

    raise HTTPException(
        status_code=403,
        detail=f"User does not have the required privileges"
    )
