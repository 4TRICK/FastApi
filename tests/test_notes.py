from fastapi.testclient import TestClient
from starlette import status

from src.app import app
from src.auth.database import get_user_id_by_email
from src.notes.database import get_note_id_by_title
from tests.conftest import get_token

client = TestClient(app)


async def test_unauthorized_create_note(drop_mock_db):
    headers = {}
    response = client.post("/notes/", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_unauthorized_get_notes(drop_mock_db):
    headers = {}
    response = client.get("/notes/", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_unauthorized_get_note(drop_mock_db):
    headers = {}
    response = client.get("/notes/12345", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_unauthorized_put_note(drop_mock_db):
    headers = {}
    response = client.put("/notes/12345", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_unauthorized_patch_note(drop_mock_db):
    headers = {}
    response = client.patch("/notes/12345", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_unauthorized_delete_note(drop_mock_db):
    headers = {}
    response = client.delete("/notes/12345", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_authorized_create_note(drop_mock_db, add_simple_user):
    bearer = get_token(client, "email@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    data = {"title": "title 1", "body": "body 1"}
    response = client.post("/notes/", headers=headers, json=data)
    assert response.status_code == status.HTTP_201_CREATED
    resp_data = response.json()
    assert resp_data["title"] == data["title"]
    assert resp_data["body"] == data["body"]
    assert resp_data["owner"] == await get_user_id_by_email("email@example.com")


async def test_authorized_get_notes(drop_mock_db, add_simple_user, add_simple_note):
    bearer = get_token(client, "email@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    response = client.get("/notes/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    resp_data = response.json()
    assert len(resp_data) == 1
    assert resp_data[0]["title"] == "title 1"
    assert resp_data[0]["body"] == "body 1"


async def test_authorized_get_empty_list_notes(drop_mock_db, add_simple_user):
    bearer = get_token(client, "email@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    response = client.get("/notes/", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_authorized_get_note(drop_mock_db, add_simple_user, add_simple_note):
    bearer = get_token(client, "email@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    note_id = await get_note_id_by_title("title 1")
    response = client.get(f"/notes/{note_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    resp_data = response.json()
    assert resp_data["title"] == "title 1"
    assert resp_data["body"] == "body 1"


async def test_authorized_get_no_exists_note(drop_mock_db, add_simple_user):
    bearer = get_token(client, "email@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    response = client.get("/notes/111111111111111111111111", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_authorized_put_note(drop_mock_db, add_simple_user, add_simple_note):
    bearer = get_token(client, "email@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    data = {"title": "title 2", "body": "body 2"}
    note_id = await get_note_id_by_title("title 1")
    response = client.put(f"/notes/{note_id}", headers=headers, json=data)
    assert response.status_code == status.HTTP_200_OK
    resp_data = response.json()
    assert resp_data["title"] == "title 2"
    assert resp_data["body"] == "body 2"


async def test_authorized_put_no_exists_note(drop_mock_db, add_simple_user):
    bearer = get_token(client, "email@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    data = {"title": "title 2", "body": "body 2"}
    response = client.put(
        f"/notes/111111111111111111111111", headers=headers, json=data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_authorized_patch_note(drop_mock_db, add_simple_user, add_simple_note):
    bearer = get_token(client, "email@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    data = {"title": "title 2", "body": "body 2"}
    note_id = await get_note_id_by_title("title 1")
    response = client.patch(f"/notes/{note_id}", headers=headers, json=data)
    assert response.status_code == status.HTTP_200_OK
    resp_data = response.json()
    assert resp_data["title"] == "title 2"
    assert resp_data["body"] == "body 2"


async def test_authorized_patch_no_exists_note(drop_mock_db, add_simple_user):
    bearer = get_token(client, "email@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    data = {"title": "title 2", "body": "body 2"}
    response = client.patch(
        f"/notes/111111111111111111111111", headers=headers, json=data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_authorized_delete_note(drop_mock_db, add_simple_user, add_simple_note):
    bearer = get_token(client, "email@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    note_id = await get_note_id_by_title("title 1")
    response = client.delete(f"/notes/{note_id}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_authorized_delete_no_exists_note(drop_mock_db, add_simple_user):
    bearer = get_token(client, "email@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    response = client.delete(f"/notes/111111111111111111111111", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
