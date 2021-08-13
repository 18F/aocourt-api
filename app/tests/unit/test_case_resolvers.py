from app.core.enums import CaseStatus
from datetime import datetime
from app.api.graph_ql.resolvers.case_resolvers import (
    case_result_type,
    resolve_docket_entries
)
from app.entities import DistrictCase, AppellateCase, DocketEntry


case_params = {
    'title': "Foreman vs Ali",
    'date_filed': datetime.now(),
    'court': 'tnmd',
    'status': CaseStatus.new
}

docket_params = {
    'case_id': 1,
    'text': "round 9",
    'court': "nysd",
    'sequence_no': 5,
    'date_filed': datetime.now(),
    'entry_type': 'ord'
}


def test_case_result_type():
    '''It should resolve to the correct string based on object'''

    d = DistrictCase(**case_params)
    assert case_result_type(d) == 'DistrictCase'

    a = AppellateCase(**case_params, original_case_id=2)
    assert case_result_type(a) == 'AppellateCase'


def test_resolve_docket_entries():
    '''It should resolve to the docket entry list on the case'''

    docket = [DocketEntry(**docket_params)]
    d = DistrictCase(**case_params, docket_entries=docket)
    resolved = resolve_docket_entries(d)
    assert resolved == docket
