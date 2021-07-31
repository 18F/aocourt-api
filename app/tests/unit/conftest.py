import pytest
from datetime import datetime
from app.core.enums import CaseStatus
from app.entities import DistrictCase


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
