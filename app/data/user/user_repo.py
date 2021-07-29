from typing import Optional, Any

from sqlalchemy.orm import Session

from app.entities import UserInput, User
from .user import User_DTO
from ..role.role import Role_DTO
from app.core.security import verify_password, get_password_hash


class CrudUser:
    '''
    Create, read, update, and delete users
    '''
    def get(self, db: Session, id: Any) -> Optional[User]:
        db_user = db.query(User_DTO).filter(User_DTO.id == id).first()
        if db_user:
            return db_user.to_entity()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        db_user = db.query(User_DTO).filter(User_DTO.email == email).first()
        if db_user:
            return db_user.to_entity()

    def create(self, db: Session, user: UserInput) -> User:
        db_roles = db.query(Role_DTO).filter(Role_DTO.rolename.in_(r.rolename for r in user.roles)).all()

        db_user = User_DTO(
            email=user.email,
            hashed_password=get_password_hash(user.password),
            roles=db_roles,
            full_name=user.full_name,
            username=user.username
        )
        db.add(db_user)
        db.commit()

        return db_user.to_entity()

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
