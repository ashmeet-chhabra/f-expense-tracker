import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

# Create table once for the whole test session (pytests's session not sqlalchemy)
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

# per-test isolated session - rolls back after every single test
@pytest.fixture
def db_session():
    connection = test_engine.connect() # open one connection
    transaction = connection.begin() # wrap everything in a transaction

    session = sessionmaker(bind=connection)()

    yield session # test runs here

    session.close()
    transaction.rollback()
    connection.close() # undo all changes for the test made

# test client that uses the isolated session instead of the real DB
@pytest.fixture
def client(db_session):
    def _override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = _override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

''' to reduce repetition of creating new user everytime after it's
 already been tested in isolation'''
@pytest.fixture
def auth_client(client):
    user = {"name":"Test","email":"Test123@gmail.com","password":"Test111"}
    client.post("/users/register", json=user)

    user = {"username":"Test123@gmail.com","password":"Test111"}
    response = client.post("/users/login", data=user)

    access_token = response.json()['access_token']

    client.headers.update({
        "Authorization": f"Bearer {access_token}"
    })

    return client
