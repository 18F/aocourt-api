import pytest
from app.core.enums import CaseStatus
from app.entities import RecordOnAppeal, Court


def test_roa_from_district_case(simple_case) -> None:
    '''
    It should create an record of appeal for this case, set the original_case_id.
    '''
    court = Court.from_id('ca9')
    roa = simple_case.create_record_on_appeal(court)
    assert isinstance(roa, RecordOnAppeal)
    assert roa.original_case_id == simple_case.id
    assert roa.receiving_court == 'ca9'
    assert roa.court == simple_case.court


def test_roa_from_district_case_no_appellate_court(simple_case) -> None:
    '''
    It should not set the receiving court automatically.
    '''
    roa = simple_case.create_record_on_appeal()
    assert roa.receiving_court == None
    assert roa.court == simple_case.court


def test_district_case_status_roa(simple_case) -> None:
    '''
    It should change status of original case to submitted_for_appeal.
    '''
    _ = simple_case.create_record_on_appeal()
    assert simple_case.status == CaseStatus.submitted_for_appeal


def test_validates_roa(simple_case) -> None:
    '''
    It should raise an exception if an record of appeal is created when one exists.
    '''
    _ = simple_case.create_record_on_appeal()
    assert simple_case.status == CaseStatus.submitted_for_appeal
    with pytest.raises(ValueError):
        _ = simple_case.create_record_on_appeal()


def test_send_roa(simple_case) -> None:
    '''
    If should set the receiving court on the record on appeal.
    '''
    roa = simple_case.create_record_on_appeal()
    roa.send_to_court(Court.from_id('ca9'))
    assert roa.receiving_court == 'ca9'
