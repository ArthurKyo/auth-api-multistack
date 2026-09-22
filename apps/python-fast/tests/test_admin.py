import os

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///./test_admin.db"
os.environ["JWT_SECRET"] = "test-secret"

from fastapi.testclient import TestClient
from app.core.security import create_access_token, hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.main import app
from app.models.user import User, UserRole

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
client = TestClient(app)

def seed_admin():
    db = SessionLocal()
    admin = User(
        name="Admin",
        email="admin@example.com",
        password_hash=hash_password("senha123"),
        role=UserRole.admin,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    token = create_access_token(str(admin.id))
    db.close()
    return token

def test_admin_can_list_users_with_pagination():
    token = seed_admin()
    response = client.get(
        "/users/admin?page=1&page_size=5",
        headers={"Authorization": "Bearer " + token},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["page"] == 1
    assert body["page_size"] == 5
    assert body["total"] >= 1
