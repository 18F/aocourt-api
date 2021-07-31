from typing import Optional, Any
from sqlalchemy.orm import Session  # , contains_eager

from app.entities import Case
from .case import run_mappers

run_mappers()


class CrudCase:
    '''
    Create, read, update, and delete cases
    '''
    def get(self, db: Session, id: Any) -> Optional[Case]:
        return db.query(Case).filter(Case.id == id).one_or_none()

    def add(self, db: Session, case):
        db.add(case)

    def create(self, db: Session, case: Case) -> Case:
        db.add(case)
        return case


case = CrudCase()
