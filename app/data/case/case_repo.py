from app.schemas.case import CaseInput
from typing import Optional, Any, Union
from pydantic import parse_obj_as
from sqlalchemy.orm import Session, contains_eager
from sqlalchemy.orm.exc import NoResultFound

from .case import DistrictCase_DTO, AppellateCase_DTO, Case_DTO
from .docket_entry import DocketEntry_DTO
from app.schemas import (
    AppellateCaseInput,
    Case as ValidCase,
)
from app.core.enums import CaseStatus


class CrudCase:
    '''
    Create, read, update, and delete cases
    '''
    def get(self, db: Session, id: Any) -> Optional[ValidCase]:
        found_case = db.query(Case_DTO).filter(Case_DTO.id == id).one_or_none()
        if found_case:
            return found_case.to_entity()

    def get_with_docket(self, db: Session, id: Any) -> Union[DistrictCase_DTO, AppellateCase_DTO]:
        original = db.query(Case_DTO).options(contains_eager(Case_DTO.docket_entries))
        original = original.outerjoin(DocketEntry_DTO).filter(Case_DTO.id == id)
        return original.one()

    def create(self, db: Session, case: CaseInput) -> Case_DTO:
        db_case = Case_DTO(**case.dict())
        db.add(db_case)
        db.commit()
        return db_case

    def set_sealed(self, db: Session, id: Any, sealed: Any) -> Optional[Union[DistrictCase_DTO, AppellateCase_DTO]]:
        case = db.query(Case_DTO).filter(Case_DTO.id == id).one_or_none()
        if case is not None:
            case.sealed = sealed
            db.add(case)
            db.commit()
        return case

    def create_appeal_case(self, db: Session, id: Any, receiving_court=None):
        '''
        Creates a new case in the original cases parent court.
        '''
        try:
            original = self.get_with_docket(db, id)
        except NoResultFound:
            raise ValueError(f"Cannot find case id: {id}")

        original_case = parse_obj_as(ValidCase, original)

        app_case = AppellateCaseInput.from_district_case(original_case, receiving_court)
        app_case.docket_entries = [DocketEntry_DTO(**d.dict()) for d in app_case.docket_entries]

        appeal = AppellateCase_DTO(**app_case.dict())
        original.status = CaseStatus.on_appeal  # type: ignore
        db.add(original)
        db.add(appeal)
        db.commit()

        return appeal


case = CrudCase()
