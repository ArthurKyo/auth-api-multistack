import os

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///./test_auth.db"
os.environ["JWT_SECRET"] = "test-secret"

from fastapi.testclient import TestClient
from app.db.base import Base
from app.db.session import engine
from app.main import app

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
client = TestClient(app)

def test_register_login_me_and_refresh():
    register = client.post("/auth/register", json={
        "name": "Arthur",
        "email": "arthur@example.com",
        "password": "senha123",
    })
    assert register.status_code == 201

    login = client.post("/auth/login", json={
        "email": "arthur@example.com",
        "password": "senha123",
    })
    assert login.status_code == 200
    tokens = login.json()

    me = client.get(
        "/users/me",
        headers={"Authorization": "Bearer " + tokens["access_token"]},
    )
    assert me.status_code == 200
    assert me.json()["email"] == "arthur@example.com"

    refresh = client.post(
        "/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert refresh.status_code == 200
    rotated = refresh.json()
    assert rotated["refresh_token"] != tokens["refresh_token"]

    reused = client.post(
        "/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert reused.status_code == 401

def test_duplicate_email_returns_conflict():
    response = client.post("/auth/register", json={
        "name": "Arthur Dois",
        "email": "arthur@example.com",
        "password": "outrasenha123",
    })
    assert response.status_code == 409

def test_invalid_login_returns_401():
    response = client.post("/auth/login", json={
        "email": "arthur@example.com",
        "password": "senhaerrada",
    })
    assert response.status_code == 401
