import pytest
from datetime import datetime
from app.core.enums import CaseStatus
from app.entities import DistrictCase, RecordOnAppeal


@pytest.fixture()
def simple_case():
    case = DistrictCase(
        title="Godzilla v. Mothra",
        date_filed=datetime.now(),
        status=CaseStatus.new,
        sealed=True,
        court="tnmd",
        docket_entries=[]
    )
    case.id = 123
    return case


@pytest.fixture
def simple_roa():
    roa = RecordOnAppeal(
        court='nysd',
        title='Predator v. Alien',
        original_case_id=123,
        date_filed=datetime.now(),
        docket_entries=[],
        receiving_court=None,
        status=CaseStatus.new
    )
    roa.id = 456
    return roa
