import json
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

headers = {"Content-Type": "application/json"}


def test_create_roa_mutation(client: TestClient, db_session: Session, simple_case) -> None:
    '''It should return a createRecordOnAppeal object with only the requested fields'''
    query = {
        "query": "mutation{createRecordOnAppeal(caseId: %d) {title, originalCaseId}}" % simple_case.id
    }
    r = client.post("/graphql/", data=json.dumps(query), headers=headers)
    assert r.status_code == 200
    resp = r.json()
    assert resp['data']['createRecordOnAppeal']['originalCaseId'] == simple_case.id
    assert resp['data']['createRecordOnAppeal']['title'] == simple_case.title


def test_create_roa_mutation_persists(client: TestClient, db_session: Session, simple_case) -> None:
    '''It should add a record of appeal to the sysyem'''
    mutation = {
        "query": "mutation{createRecordOnAppeal(caseId: %d) {id, title, originalCaseId}}" % simple_case.id
    }
    r = client.post("/graphql/", data=json.dumps(mutation), headers=headers)
    resp = r.json()
    roa_id = resp['data']['createRecordOnAppeal']['id']

    query = {
        "query": "{recordOnAppeal(id: %s) {id, title, originalCaseId}}" % roa_id
    }
    r = client.post("/graphql/", data=json.dumps(query), headers=headers)
    assert r.status_code == 200
    resp = r.json()
    assert resp['data'] == {
        'recordOnAppeal': {
            'id': roa_id,
            'title': simple_case.title,
            'originalCaseId': simple_case.id
        }
    }


def test_send_roa_persists(client: TestClient, db_session: Session, simple_case) -> None:
    '''It should add a record of appeal to the sysyem'''
    create_mutation = {
        "query": "mutation{createRecordOnAppeal(caseId: %d) {id, title, originalCaseId}}" % simple_case.id
    }
    r = client.post("/graphql/", data=json.dumps(create_mutation), headers=headers)
    resp = r.json()
    roa_id = resp['data']['createRecordOnAppeal']['id']

    send_mutation = {
        "query": '''
            mutation{sendRecordOnAppeal(recordOnAppealId: %s, receivingCourtId: "ca9") {
                id,
                receivingCourt{
                    id
                } }}''' % roa_id
    }

    r = client.post("/graphql/", data=json.dumps(send_mutation), headers=headers)
    assert r.status_code == 200
    resp = r.json()
    assert resp['data'] == {
        'sendRecordOnAppeal': {
            'id': roa_id,
            'receivingCourt': {'id': 'ca9'}
        }
    }
