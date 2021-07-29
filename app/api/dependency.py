from typing import Iterable

from pydantic import ValidationError
from fastapi import Depends, HTTPException, status
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.data import User_DTO, user
from app.schemas import TokenPayload
from app.core import security
from app.data.database import get_db

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User_DTO:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    current_user = user.get(db, id=token_data.sub)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return current_user


def get_current_active_user(current_user: User_DTO = Depends(get_current_user)) -> User_DTO:
    if not user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class AllowRoles():
    def __init__(self, roles: Iterable[str]):
        self.autorized_roles = list(roles)

    def __call__(self, user: User_DTO = Depends(get_current_active_user)) -> User_DTO:
        if not any(role.rolename in self.autorized_roles for role in user.roles):
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return user
