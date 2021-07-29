from datetime import datetime
from app.api.graph_ql.resolvers.case import case_result_type, resolve_docket_entries
from app.entities import DistrictCase, AppellateCase, DocketEntry


case_params = {
    'id': 1,
    'title': "Foreman vs Ali",
    'created_at': datetime.now(),
    'date_filed': datetime.now(),
    'updated_on': datetime.now(),
    'court': 'tnmd'
}

docket_params = {
    'id': 50,
    'case_id': 1,
    'created_at': datetime.now(),
    'updated_on': datetime.now(),
    'text': "round 9",
    'sequence_no': 5,
    'date_filed': datetime.now(),
    'entry_type': 'ord'
}


def test_case_result_type():
    '''It should resolve to the correct string based on object'''

    d = DistrictCase(**case_params, type='district')
    assert case_result_type(d) == 'DistrictCase'

    a = AppellateCase(**case_params, type='appellate', original_case_id=2)
    assert case_result_type(a) == 'AppellateCase'


def test_resolve_docket_entries():
    '''It should resolve to the docket entry list on the case'''

    docket = [DocketEntry(**docket_params)]
    d = DistrictCase(**case_params, type='district', docket_entries=docket)
    resolved = resolve_docket_entries(d)
    assert resolved == docket
