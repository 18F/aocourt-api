from typing import Optional, Any

from sqlalchemy.orm import Session

from app.entities import RoleInput
from ..role.role import Role_DTO


class CrudRole:
    '''
    Create, read, update, and delete roles
    '''
    def get(self, db: Session, id: Any) -> Optional[Role_DTO]:
        return db.query(Role_DTO).filter(Role_DTO.id == id).first()

    def get_by_name(self, db: Session, rolename: Any) -> Optional[Role_DTO]:
        return db.query(Role_DTO).filter(Role_DTO.rolename == rolename).first()

    def create(self, db: Session, role: RoleInput) -> Role_DTO:
        db_role = Role_DTO(**role.dict())
        db.add(db_role)
        db.commit()
        return db_role


role = CrudRole()
