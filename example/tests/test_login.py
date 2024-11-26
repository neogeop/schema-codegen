import pytest
from sqlalchemy.future import select
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer
from example.config import Settings
from example.db import get_session_factory, get_engine, get_settings
from example.http import pwd_context
from example.models.db import Users, LoginSessions
from example.main import app
from schema_codegen.migrations import apply_migrations


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:latest") as postgres:
        yield postgres

@pytest.fixture(scope="session")
def test_settings(postgres_container):
    Settings.DATABASE_URL = postgres_container.get_connection_url()
    return Settings

@pytest.fixture(scope="session")
def test_apply_migrations(test_settings):
    apply_migrations("migrations", test_settings.DATABASE_URL)

@pytest.fixture(scope="session")
def test_app(test_settings):
    app.dependency_overrides[get_settings] = lambda: test_settings
    return app

@pytest.fixture(scope="session")
def test_db_session(test_app, test_apply_migrations, test_settings):
    engine = get_engine(test_settings)
    session_gen = get_session_factory(engine)
    with session_gen() as session:
        yield session

@pytest.fixture(scope="session")
def test_user(test_db_session):
    user = Users(
        username="test_user",
        password_hash=pwd_context.hash("correct_password")
    )
    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)
    
    yield user
    
    test_db_session.delete(user)
    test_db_session.commit()

@pytest.fixture(scope="session")
def test_client(test_app):
    return TestClient(test_app)

def test_login_success(test_db_session, test_user, test_client):
    plain_password = "correct_password"
    test_db_session.commit()

    user_data = {
        "username": "test_user",
        "password": plain_password
    }

    # Send login request
    response = test_client.post("/api/login", json=user_data)

    # Assert successful login
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Login successful"
    
    # Verify the login session was created
    stmt = select(LoginSessions).join(Users).filter(Users.username == "test_user")
    result = test_db_session.execute(stmt)
    login_session = result.scalars().first()

    # Assert that a login session was created
    assert login_session is not None
    assert login_session.user_id == test_user.id
    assert login_session.created_at is not None

    # Cleanup login session
    test_db_session.delete(login_session)
    test_db_session.commit()
