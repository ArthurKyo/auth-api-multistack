from app.core.security import create_access_token, hash_password
from app.models.user import User, UserRole


def seed_user(db, email: str, role: UserRole = UserRole.user):
    user = User(
        name=email.split("@")[0],
        email=email,
        password_hash=hash_password("senha123"),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_admin_can_list_users_with_pagination(client, db):
    admin = seed_user(db, "admin@example.com", UserRole.admin)
    for index in range(12):
        seed_user(db, f"user{index}@example.com")

    token = create_access_token(str(admin.id))

    response = client.get(
        "/users/admin?page=2&page_size=5",
        headers={"Authorization": "Bearer " + token},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["page"] == 2
    assert body["page_size"] == 5
    assert body["total"] == 13
    assert len(body["items"]) == 5


def test_regular_user_cannot_list_users(client, db):
    user = seed_user(db, "user@example.com", UserRole.user)
    token = create_access_token(str(user.id))

    response = client.get(
        "/users/admin",
        headers={"Authorization": "Bearer " + token},
    )

    assert response.status_code == 403
