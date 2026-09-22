def register_user(client, email="arthur@example.com"):
    return client.post(
        "/auth/register",
        json={
            "name": "Arthur",
            "email": email,
            "password": "senha123",
        },
    )


def login_user(client, email="arthur@example.com", password="senha123"):
    return client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )


def test_register_login_me_refresh_and_logout(client):
    register = register_user(client)
    assert register.status_code == 201
    assert register.json()["email"] == "arthur@example.com"
    assert "password" not in register.json()
    assert "password_hash" not in register.json()

    login = login_user(client)
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

    logout = client.post(
        "/auth/logout",
        json={"refresh_token": rotated["refresh_token"]},
    )
    assert logout.status_code == 204

    after_logout = client.post(
        "/auth/refresh",
        json={"refresh_token": rotated["refresh_token"]},
    )
    assert after_logout.status_code == 401


def test_duplicate_email_returns_conflict(client):
    assert register_user(client).status_code == 201

    response = register_user(client)

    assert response.status_code == 409


def test_invalid_login_returns_401(client):
    assert register_user(client).status_code == 201

    response = login_user(client, password="senhaerrada")

    assert response.status_code == 401


def test_protected_endpoint_rejects_missing_token(client):
    response = client.get("/users/me")

    assert response.status_code in (401, 403)


def test_login_rate_limit_returns_429(client):
    assert register_user(client).status_code == 201

    for _ in range(5):
        response = login_user(client, password="errada123")
        assert response.status_code == 401

    blocked = login_user(client, password="errada123")
    assert blocked.status_code == 429
    assert blocked.headers["retry-after"]
