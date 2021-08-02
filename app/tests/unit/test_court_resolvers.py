from unittest.mock import patch
import pytest
from app.api.graph_ql.resolvers.court_resolvers import resolve_lower_courts
from app.entities import Court


fake_courts = {
    'app': {'type': 'appellate',
            'full_name': 'Some Appellate Court',
            'parent': None,
            'short_name': 'Cicuit 1'},
    'd1': {'type': 'district',
           'full_name': 'a district court',
           'parent': 'app',
           'short_name': 'D. one'},
    'd2': {'type': 'district',
           'full_name': 'another distirct court',
           'parent': 'app',
           'short_name': 'D. Two'},
    'd3': {'type': 'district',
           'full_name': 'yet another distirct court',
           'parent': 'app4',
           'short_name': 'D. Three'},
    'app2': {'type': 'appellate',
             'full_name': 'Some Other Appellate Court',
             'parent': None,
             'short_name': 'Cicuit 2'}
}


@patch('app.api.graph_ql.resolvers.court_resolvers.courts', fake_courts)
def test_resolve_lower_courts():
    '''It should resolve to a list of lower courts under the given court'''
    c = Court(**fake_courts['app'], id='app')
    resolved = resolve_lower_courts(c)
    assert resolved == [
        Court(**fake_courts['d1'], id='d1'),
        Court(**fake_courts['d2'], id='d2')
    ]


@patch('app.api.graph_ql.resolvers.court_resolvers.courts', fake_courts)
@pytest.mark.parametrize('court_id', ['app2', 'd1'])
def test_resolve_no_lower_courts(court_id):
    '''It should resolve to an empty list when there are no lower courts'''
    c = Court(**fake_courts[court_id], id=court_id)
    resolved = resolve_lower_courts(c)
    assert resolved == []
