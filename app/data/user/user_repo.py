from typing import Optional, Any

from sqlalchemy.orm import Session

from app.entities import User
from app.core.security import verify_password
from .user import run_mappers

run_mappers()


class CrudUser:
    '''
    Create, read, update, and delete users
    '''
    def get(self, db: Session, id: Any) -> Optional[User]:
        return db.query(User).filter(User.id == id).one_or_none()

    def add(self, db: Session, user: User):
        db.add(user)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).one_or_none()

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active


user = CrudUser()
