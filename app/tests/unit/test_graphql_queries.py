from unittest.mock import MagicMock, Mock, patch, ANY

from app.api.graph_ql.resolvers.query_resolvers import resolve_case, resolve_roa


@patch('app.api.graph_ql.resolvers.query_resolvers.case')
def test_case_resolver(case_patch, simple_case):
    '''It should return the case provided by the database'''
    info = MagicMock()
    case_patch.get = Mock(return_value=simple_case)
    assert resolve_case({}, info, id=1) == simple_case
    case_patch.get.assert_called_with(ANY, 1)


@patch('app.api.graph_ql.resolvers.query_resolvers.case')
def test_case_query_not_found(case_patch):
    '''It should return None if the database returns None'''
    info = MagicMock()
    case_patch.get = Mock(return_value=None)
    assert resolve_case({}, info, id=1) is None


@patch('app.api.graph_ql.resolvers.query_resolvers.record_on_appeal')
def test_roa_resolver(roa_patch, simple_roa):
    '''It should return roa if the database returns None'''
    info = MagicMock()
    roa_patch.get = Mock(return_value=simple_roa)
    assert resolve_roa({}, info, id=10) == simple_roa


@patch('app.api.graph_ql.resolvers.query_resolvers.record_on_appeal')
def test_roa_resolver_not_found(roa_patch, simple_roa):
    '''It should return roa if the database returns None'''
    info = MagicMock()
    roa_patch.get = Mock(return_value=None)
    assert resolve_roa({}, info, id=10) is None
