from sqlalchemy.orm import Session

from app.data_service import case
from app.core.enums import CourtType, CaseStatus


def test_appeal_case(db_session: Session, simple_case) -> None:
    '''
    It should create an appellate case, set the original_case_id and
    change the original case status.
    '''
    appeal = case.create_appeal_case(db_session, simple_case.id)
    assert appeal.type == CourtType.appellate
    assert appeal.original_case_id == simple_case.id
    assert simple_case.status == CaseStatus.on_appeal
