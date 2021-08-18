from app.core.enums import CaseStatus
from typing import Generator, Any
from datetime import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.data.database import mapper_registry, get_db
from sqlalchemy.orm import sessionmaker
from app.entities import User, DistrictCase
from app.core.security import get_password_hash, create_access_token

engine = create_engine(settings.DATABASE_URL_TEST)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True, scope="package")
def api_app() -> Generator[FastAPI, Any, None]:
    '''Set up tables for the tests'''
    mapper_registry.metadata.create_all(engine)
    yield app
    mapper_registry.metadata.drop_all(engine)


@pytest.fixture
def db_session(api_app: FastAPI) -> Generator[Session, Any, None]:
    '''Create a fresh session inside a transacation and roll it back after the test'''
    connection = engine.connect()
    transaction = connection.begin()
    session = TestSession(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(api_app: FastAPI, db_session: Session) -> Generator[TestClient, Any, None]:
    '''Uses FastAPIs dependency injection to replace the DB dependency everywhere'''

    def get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def default_user(db_session: Session):
    hashed_password = get_password_hash(settings.INITIAL_ADMIN_PASSWORD)

    test_user = User(
        email=settings.INITIAL_ADMIN_USER,
        hashed_password=hashed_password,
        full_name="Test User",
        username="user.test",
        roles=[]
    )

    db_session.add(test_user)
    db_session.commit()
    return test_user


@pytest.fixture()
def simple_case(db_session: Session):
    case_in = DistrictCase(
        title="Godzilla v. Mothra",
        date_filed=datetime.now(),
        status=CaseStatus.new,
        sealed=True,
        court="tnmd",
        docket_entries=[]
    )
    db_session.add(case_in)
    db_session.commit()
    return case_in


@pytest.fixture()
def admin_token():
    return create_access_token('1')
