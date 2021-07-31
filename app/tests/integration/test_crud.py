from sqlalchemy.orm import Session

from app.entities import AppellateCase
from app.core.enums import CourtType


def test_appeal_case(db_session: Session, simple_case) -> None:
    '''
    It should create an appellate case, set the original_case_id and
    change the original case status.
    '''
    appeal = AppellateCase.from_district_case(simple_case, 'ca9')
    assert appeal.type == CourtType.appellate
    assert appeal.original_case_id == simple_case.id
