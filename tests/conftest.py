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
@pytest.fixture()
def db_session():
    connection = test_engine.connect() # open one connection
    transaction = connection.begin() # wrap everything in a transaction

    session = sessionmaker(bind=connection)()

    yield session # test runs here

    session.close()
    transaction.rollback()
    connection.close() # undo all changes for the test made

# test client that uses the isolated session instead of the real DB
@pytest.fixture()
def client(db_session):
    def _override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = _override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()