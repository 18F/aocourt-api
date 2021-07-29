from typing import Optional, Any
from sqlalchemy.orm import Session, contains_eager
from sqlalchemy.orm.exc import NoResultFound

from .case import AppellateCase_DTO, Case_DTO
from .docket_entry import DocketEntry_DTO
from app.entities import (
    AppellateCaseInput,
    CaseInput,
    Case
)
from app.core.enums import CaseStatus


class CrudCase:
    '''
    Create, read, update, and delete cases
    '''
    def get(self, db: Session, id: Any) -> Optional[Case]:
        found_case = db.query(Case_DTO).filter(Case_DTO.id == id).one_or_none()
        if found_case:
            return found_case.to_entity()

    def create(self, db: Session, case: CaseInput) -> Case_DTO:
        db_case = Case_DTO(**case.dict())
        db.add(db_case)
        db.commit()
        return db_case

    def set_sealed(self, db: Session, id: Any, sealed: Any) -> Optional[Case]:
        case = db.query(Case_DTO).filter(Case_DTO.id == id).one_or_none()
        if case is not None:
            case.sealed = sealed
            db.add(case)
            db.commit()
            return case.to_entity()

    def create_appeal_case(self, db: Session, id: Any, receiving_court=None) -> Case:
        '''
        Creates a new case in the original cases parent court.
        '''
        try:
            original = db.query(Case_DTO).options(contains_eager(Case_DTO.docket_entries)) \
                .outerjoin(DocketEntry_DTO).filter(Case_DTO.id == id) \
                .one()
        except NoResultFound:
            raise ValueError(f"Cannot find case id: {id}")

        original_case = original.to_entity()

        app_case = AppellateCaseInput.from_district_case(original_case, receiving_court)
        app_case.docket_entries = [DocketEntry_DTO(**d.dict()) for d in app_case.docket_entries]

        appeal = AppellateCase_DTO(**app_case.dict())
        original.status = CaseStatus.on_appeal  # type: ignore
        db.add(original)
        db.add(appeal)
        db.commit()

        return appeal.to_entity()


case = CrudCase()
