from fastapi.testclient import TestClient
from starlette import status

from src.app import app
from tests.conftest import get_token

client = TestClient(app)


async def test_register_new_user(drop_mock_db):
    data = {"email": "email@example.com", "password": "password"}
    response = client.post("/auth/register", json=data)
    resp_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert resp_data["email"] == data["email"]


async def test_register_new_admin_user(drop_mock_db):
    data = {"email": "email@example.com", "password": "password", "is_admin": True}
    response = client.post("/auth/register", json=data)
    resp_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert resp_data["email"] == data["email"]
    assert resp_data["is_admin"] == data["is_admin"]


async def test_register_existing_user(drop_mock_db, add_simple_user):
    data = {"email": "email@example.com", "password": "password"}
    response = client.post("/auth/register", json=data)
    assert response.status_code == status.HTTP_409_CONFLICT


async def test_token_existing_user(drop_mock_db, add_simple_user):
    data = {"email": "email@example.com", "password": "password"}
    response = client.post("/auth/token", json=data)
    assert response.status_code == status.HTTP_200_OK
    resp_data = response.json()
    assert "access_token" in resp_data
    assert "token_type" in resp_data


async def test_token_not_existing_user(drop_mock_db, add_simple_user):
    data = {"email": "not_exist_email@example.com", "password": "password"}
    response = client.post("/auth/token", json=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_token_wrong_password_user(drop_mock_db, add_simple_user):
    data = {"email": "email@example.com", "password": "wrong_password"}
    response = client.post("/auth/token", json=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_access_with_valid_bearer(drop_mock_db, add_simple_user):
    bearer = get_token(client, "email@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    response = client.get("/auth/user", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    resp_data = response.json()
    assert resp_data["email"] == "email@example.com"


async def test_access_with_invalid_bearer(drop_mock_db, add_simple_user):
    bearer = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlbWFpbDRAZXhhbXBsZS5ydSIsImV4cCI6MTcyOTI4NzA1NH0.Et2La33oyYxEA8MKvuaRVH2KxiK5aRhgu8r2WMsBqdE"
    headers = {"Authorization": f"Bearer {bearer}"}
    response = client.get("/auth/user", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_access_without_authorization(drop_mock_db, add_simple_user):
    headers = {}
    response = client.get("/auth/user", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
