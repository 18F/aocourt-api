from app.schemas.case import CaseInput
from typing import Optional, Any, Union
from pydantic import parse_obj_as
from sqlalchemy.orm import Session, contains_eager
from sqlalchemy.orm.exc import NoResultFound

from app.models import DistrictCase, AppellateCase, Case, DocketEntry
from app.schemas import (
    DistrictCase as ValidDistrictCase,
    AppellateCaseInput,
    Case as ValidCase,
    Court
)
from app.core.courts import courts
from app.core.enums import CaseStatus


class CrudCase:
    '''
    Create, read, update, and delete cases
    '''
    def get(self, db: Session, id: Any) -> Optional[Union[DistrictCase, AppellateCase]]:
        return db.query(Case).filter(Case.id == id).one_or_none()

    def get_with_docket(self, db: Session, id: Any) -> Union[DistrictCase, AppellateCase]:
        original = db.query(Case).options(contains_eager(Case.docket_entries))
        original = original.outerjoin(DocketEntry).filter(Case.id == id)
        return original.one()

    def create(self, db: Session, case: CaseInput) -> Case:
        db_case = Case(**case.dict())
        db.add(db_case)
        db.commit()
        return db_case

    def set_sealed(self, db: Session, id: Any, sealed: Any) -> Optional[Union[DistrictCase, AppellateCase]]:
        case = db.query(Case).filter(Case.id == id).one_or_none()
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

        if receiving_court is None:
            sending_court = courts[original_case.court]
            receiving_court = sending_court['parent']
        appellate_court = Court(id=receiving_court, **courts[receiving_court])

        original_case.validate_appeal(appellate_court)

        appellate = original_case.dict(exclude={'id', 'type'})
        appellate['original_case_id'] = original_case.id
        appellate['court'] = receiving_court
        app_case = AppellateCaseInput(**appellate)
        app_case.docket_entries = [DocketEntry(**d.dict()) for d in app_case.docket_entries]

        appeal = AppellateCase(**app_case.dict())
        original.status = CaseStatus.on_appeal  # type: ignore
        db.add(original)
        db.add(appeal)
        db.commit()

        return appeal

    def send_roa(self, db: Session, id: Any) -> Optional[AppellateCase]:
        # For now just grab orders to demonstrate filtering
        # This will probably need to allow specific filtering of docket items
        original = db.query(Case).options(contains_eager(Case.docket_entries))
        original = original.join(DocketEntry).filter(Case.id == id).filter(DocketEntry.entry_type == 'order')
        original = original.one_or_none()
        if original is None:
            return
        # make an appeal
        # this raises a ValidationError if the original is not
        # a proper district case
        valid_case = ValidDistrictCase.from_orm(original)

        appellate = valid_case.dict(exclude={'id', 'type'})
        appellate['original_case_id'] = valid_case.id
        app_case = AppellateCaseInput(**appellate)
        app_case.docket_entries = [DocketEntry(**d.dict()) for d in app_case.docket_entries]

        appeal = AppellateCase(**app_case.dict())
        db.add(appeal)
        db.commit()

        return appeal


case = CrudCase()
