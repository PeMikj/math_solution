import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models import User, Problem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def test_user(test_db):
    db = TestingSessionLocal()
    user = User(username="testuser", hashed_password="testpassword")
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

@pytest.fixture(scope="module")
def test_problem(test_user):
    db = TestingSessionLocal()
    problem = Problem(user_id=test_user.id, problem_text="Test problem", known_answer="Test answer", status="pending")
    db.add(problem)
    db.commit()
    db.refresh(problem)
    db.close()
    return problem

def test_get_problems(test_user, test_problem):
    response = client.get("/problems/", headers={"Authorization": f"Bearer {test_user.id}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["problem_text"] == "Test problem"
    assert data[0]["status"] == "pending"

def test_create_problem(test_user):
    problem_data = {
        "problem_text": "New test problem",
        "known_answer": "New test answer"
    }
    response = client.post("/problems/", json=problem_data, headers={"Authorization": f"Bearer {test_user.id}"})
    assert response.status_code == 200
    data = response.json()
    assert data["problem_text"] == "New test problem"
    assert data["known_answer"] == "New test answer"
    assert data["status"] == "pending"

def test_unauthorized_access():
    response = client.get("/problems/")
    assert response.status_code == 401

def test_get_problems_for_specific_user(test_user, test_problem):
    another_user = User(username="anotheruser", hashed_password="anotherpassword")
    db = TestingSessionLocal()
    db.add(another_user)
    db.commit()
    db.refresh(another_user)
    db.close()

    response = client.get("/problems/", headers={"Authorization": f"Bearer {another_user.id}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0