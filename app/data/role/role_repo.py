from typing import Optional, Any

from sqlalchemy.orm import Session
from app.entities import Role
from .role import run_mappers

run_mappers()


class CrudRole:
    '''
    Create, read, update, and delete roles
    '''
    def get(self, db: Session, id: Any) -> Optional[Role]:
        return db.query(Role).filter(Role.id == id).first()

    def get_by_name(self, db: Session, rolename: Any) -> Optional[Role]:
        return db.query(Role).filter(Role.rolename == rolename).first()

    def create(self, db: Session, role: Role) -> Role:
        db.add(role)
        return role


role = CrudRole()
