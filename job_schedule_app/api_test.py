import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from .database import Base
from .main import app, get_db
from .init_db import load_data_into_db
from . import models, schemas

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

test_client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def before_all():
    """
    initialize the test database
    """
    test_client.get("/initDatabase?isTest=true")


def test_get_jobs():
    response = test_client.get("/jobs")
    assert response.status_code == 200
    response_json = response.json()
    assert "total" in response_json
    assert response_json["total"] == 15
    assert "size" in response_json
    assert response_json["size"] == 10  # default limit
    assert "offset" in response_json
    assert response_json["offset"] == 0
    assert "limit" in response_json
    assert response_json["limit"] == 10
    assert "jobs" in response_json


def test_get_jobs_limit_offset():
    response = test_client.get("/jobs?limit=5&offset=10")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["size"] == 5
    assert response_json["offset"] == 10
    # offset by 10 (id is auto-increment)
    assert response_json["jobs"][0]["id"] == 11


def test_get_jobs_filter_by_talent_id():
    response = test_client.get("/jobs?filterByTalentId=tln_6164")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["size"] == 2
    assert response_json["jobs"][0]["talent_id"] == "tln_6164"


def test_get_jobs_filter_by_client_id():
    response = test_client.get("/jobs?filterByClientId=cl_2")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["size"] == 1
    assert response_json["jobs"][0]["client_id"] == "cl_2"
    assert response_json["jobs"][0]["client"]["industry"] == "AI"


def test_get_jobs_search_by_operating_unit():
    response = test_client.get("/jobs?searchByOperatingUnit=3")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["size"] == 3
    assert response_json["jobs"][0]["operating_unit"] == "Operating Unit 3"


def test_get_jobs_order_by_job_manager_ascending():
    response = test_client.get("/jobs?orderByManagertName=asc")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["jobs"][0]["job_manager_name"] == "Annamaria Heß"


def test_get_jobs_order_by_job_manager_descending():
    response = test_client.get("/jobs?orderByManagertName=desc")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["jobs"][0]["job_manager_name"] == "Yasemin Ullmann"
