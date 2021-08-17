import json
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

headers = {"Content-Type": "application/json"}


def test_basic_graphql_query(client: TestClient, db_session: Session, simple_case) -> None:
    '''It should return a case with only the requested fields'''
    query = {
        "query": "{case(id: %d) {title, type}}" % simple_case.id
    }

    r = client.post("/graphql/", data=json.dumps(query), headers=headers)
    assert r.status_code == 200
    resp = r.json()
    assert resp['data']['case']['title'] == 'Godzilla v. Mothra'
    assert resp['data']['case']['type'] == 'district'
    assert 'sealed' not in resp['data']['case']


def test_graphql_no_match_query(client: TestClient, db_session: Session, simple_case) -> None:
    '''It should return a case as none if not found'''
    query = {
        "query": "{case(id: 999) {title, type}}"
    }

    r = client.post("/graphql/", data=json.dumps(query), headers=headers)
    assert r.status_code == 200
    resp = r.json()
    assert resp['data']['case'] is None


def test_graphql_invalid_query(client: TestClient, db_session: Session, simple_case) -> None:
    '''Given invalid an query, it should return http 400  with errors in result'''
    query = {
        "query": "{case(id: 999) {bad_field, type}}"
    }

    r = client.post("/graphql/", data=json.dumps(query), headers=headers)
    assert r.status_code == 400
    resp = r.json()
    assert 'data' not in resp
    assert resp['errors'] is not None


def test_private_graphql_query_no_token(client: TestClient, db_session: Session, simple_case) -> None:
    '''It should return a 401 error when trying to reach private endpoint without a token'''
    query = {
        "query": "{case(id: %d) {title, type}}" % simple_case.id
    }

    r = client.post("/graphql_private/", data=json.dumps(query), headers=headers)
    assert r.status_code == 401


def test_private_graphql_query_good_token(client: TestClient, db_session: Session, simple_case, admin_token) -> None:
    '''It should return data with a good token'''
    query = {
        "query": "{case(id: %d) {title, type}}" % simple_case.id
    }

    r = client.post(
        "/graphql/",
        data=json.dumps(query),
        headers={**headers, 'Authorization': f'Bearer {admin_token}'}
    )
    assert r.status_code == 200
    resp = r.json()
    assert resp['data']['case']['title'] == 'Godzilla v. Mothra'
