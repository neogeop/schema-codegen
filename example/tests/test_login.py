import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.future import select
from fastapi import Depends
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer
from example.config import Settings
from example.db import get_db, get_session_factory, get_engine, get_settings
from example.http import pwd_context
from example.models.db import User, LoginSession
from example.main import app
from schema_codegen.migrations import apply_migrations


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:latest") as postgres:
        yield postgres

@pytest.fixture(scope="session")
def test_settings(postgres_container):
    database_url = postgres_container.get_connection_url()
    apply_migrations("migrations", database_url)
    Settings.DATABASE_URL = database_url
    return Settings

@pytest.fixture(scope="session")
def test_engine(test_settings):
    engine = create_engine(test_settings.DATABASE_URL, echo=True)
    yield engine
    engine.dispose()

@pytest.fixture(scope="session")
def test_session_factory(test_engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session")
def test_db_session(test_session_factory):
    yield test_session_factory()

@pytest.fixture(scope="session")
def override_test_dependencies(test_engine, test_settings, test_session_factory):
    app.dependency_overrides[get_settings] = lambda: test_settings
    app.dependency_overrides[get_engine] = lambda: test_engine
    app.dependency_overrides[get_session_factory] = lambda: test_session_factory
    return app


@pytest.fixture(scope="session")
def test_user(test_db_session):
    user = User(
        username="test_user",
        password_hash=pwd_context.hash("correct_password")
    )
    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)
    
    yield user
    
    test_db_session.delete(user)
    test_db_session.commit()


def test_login_success(test_db_session, test_user, override_test_dependencies):
    client = TestClient(override_test_dependencies)

    plain_password = "correct_password"
    test_db_session.commit()

    user_data = {
        "username": "test_user",
        "password": plain_password
    }

    # Send login request
    response = client.post("/api/login", json=user_data)

    # Assert successful login
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Login successful"
    
    # Verify the login session was created
    stmt = select(LoginSession).join(User).filter(User.username == "test_user")
    result = test_db_session.execute(stmt)
    login_session = result.scalars().first()

    # Assert that a login session was created
    assert login_session is not None
    assert login_session.user_id == test_user.id
    assert login_session.created_at is not None

    # Cleanup login session
    test_db_session.delete(login_session)
    test_db_session.commit()
