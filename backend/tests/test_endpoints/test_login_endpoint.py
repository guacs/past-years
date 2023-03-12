"""Tests for the login endpoint."""

from falcon.testing import TestClient

from tests.utils import MockUser


def test_login_valid_creds(client: TestClient, existing_user: MockUser):
    payload = {"email": existing_user.email, "password": existing_user.password}
    resp = client.simulate_post("/login", json=payload)
    resp_payload = resp.json  # type: ignore
    expected_keys = ("access_token", "refresh_token", "user")

    assert resp.status_code == 200
    assert all(key in resp_payload for key in expected_keys)
    assert resp_payload["access_token"]
    assert resp_payload["refresh_token"]

    user = resp_payload["user"]
    assert user["user_id"] == existing_user.user_id
    assert user["display_name"] == existing_user.display_name
    assert user["email"] == existing_user.email


def test_login_invalid_email(client: TestClient):
    payload = {"email": "invalid", "password": "invalid"}
    resp = client.simulate_post("/login", json=payload)

    assert resp.status_code == 401


def test_login_invalid_password(client: TestClient, existing_user: MockUser):
    payload = {"email": existing_user.email, "password": "invalid"}
    resp = client.simulate_post("/login", json=payload)

    assert resp.status_code == 401


def test_missing_values_in_payload(client: TestClient):
    payload = {"email": "some email"}
    resp = client.simulate_post("/login", json=payload)

    assert resp.status_code == 400

    payload = {"password": "some pwd"}
    resp = client.simulate_post("/login", json=payload)

    assert resp.status_code == 400


def test_logout(client: TestClient):
    resp = client.simulate_get("/logout/2")

    assert resp.status_code == 200
