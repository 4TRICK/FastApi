from fastapi.testclient import TestClient
from starlette import status

from src.app import app
from src.notes.database import get_note_id_by_title
from tests.conftest import get_token

client = TestClient(app)


async def test_authorized_get_owner_notes(
    drop_mock_db, add_3_simple_users, add_3_simple_notes
):
    bearer = get_token(client, "email1@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    response = client.get("/notes/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    resp_data = response.json()
    assert len(resp_data) == 2


async def test_authorized_get_owner_notes_empty(
    drop_mock_db, add_3_simple_users, add_3_simple_notes
):
    bearer = get_token(client, "email3@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    response = client.get("/notes/", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_authorized_get_owner_note(
    drop_mock_db, add_3_simple_users, add_3_simple_notes
):
    bearer = get_token(client, "email1@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    note_id = await get_note_id_by_title("title 1")
    response = client.get(f"/notes/{note_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK


async def test_authorized_get_not_owner_note(
    drop_mock_db, add_3_simple_users, add_3_simple_notes
):
    bearer = get_token(client, "email2@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    note_id = await get_note_id_by_title("title 1")
    response = client.get(f"/notes/{note_id}", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_authorized_put_owner_note(
    drop_mock_db, add_3_simple_users, add_3_simple_notes
):
    bearer = get_token(client, "email1@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    data = {"title": "title 11", "body": "body 11"}
    note_id = await get_note_id_by_title("title 1")
    response = client.put(f"/notes/{note_id}", headers=headers, json=data)
    assert response.status_code == status.HTTP_200_OK


async def test_authorized_put_not_owner_note(
    drop_mock_db, add_3_simple_users, add_3_simple_notes
):
    bearer = get_token(client, "email2@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    data = {"title": "title 11", "body": "body 11"}
    note_id = await get_note_id_by_title("title 1")
    response = client.put(f"/notes/{note_id}", headers=headers, json=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_authorized_patch_owner_note(
    drop_mock_db, add_3_simple_users, add_3_simple_notes
):
    bearer = get_token(client, "email1@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    data = {"body": "body 11"}
    note_id = await get_note_id_by_title("title 1")
    response = client.patch(f"/notes/{note_id}", headers=headers, json=data)
    assert response.status_code == status.HTTP_200_OK


async def test_authorized_patch_not_owner_note(
    drop_mock_db, add_3_simple_users, add_3_simple_notes
):
    bearer = get_token(client, "email2@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    data = {"body": "body 11"}
    note_id = await get_note_id_by_title("title 1")
    response = client.patch(f"/notes/{note_id}", headers=headers, json=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_authorized_delete_owner_note(
    drop_mock_db, add_3_simple_users, add_3_simple_notes
):
    bearer = get_token(client, "email1@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    note_id = await get_note_id_by_title("title 1")
    response = client.delete(f"/notes/{note_id}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_authorized_delete_not_owner_note(
    drop_mock_db, add_3_simple_users, add_3_simple_notes
):
    bearer = get_token(client, "email2@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    note_id = await get_note_id_by_title("title 1")
    response = client.delete(f"/notes/{note_id}", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
