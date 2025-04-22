import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel
from app.main import app, engine  

@pytest.fixture(scope="session", autouse=True)
def db_setup():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
