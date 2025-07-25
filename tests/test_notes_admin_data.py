from fastapi.testclient import TestClient
from starlette import status

from src.app import app
from src.auth.database import get_user_id_by_email
from src.notes.database import get_note_id_by_title
from tests.conftest import get_token

client = TestClient(app)


async def test_authorized_as_admin_create_note(drop_mock_db, add_3_simple_users):
    bearer = get_token(client, "admin@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    data = {"title": "title 1", "body": "body 1"}
    response = client.post("/notes/", headers=headers, json=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_authorized_as_admin_get_notes(
    drop_mock_db, add_3_simple_users, add_3_simple_notes
):
    bearer = get_token(client, "admin@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    response = client.get("/notes/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    resp_data = response.json()
    assert len(resp_data) == 3


async def test_authorized_as_admin_get_notes_current_owner(
    drop_mock_db, add_3_simple_users, add_3_simple_notes
):
    bearer = get_token(client, "admin@example.com", "password")
    owner_user_id = await get_user_id_by_email("email1@example.com")
    headers = {"Authorization": f"Bearer {bearer}"}
    params = {"notes_user_id": f"{owner_user_id}"}
    response = client.get("/notes/", headers=headers, params=params)
    assert response.status_code == status.HTTP_200_OK
    resp_data = response.json()
    assert len(resp_data) == 2


async def test_authorized_as_simpe_get_notes_current_owner(
    drop_mock_db, add_3_simple_users, add_3_simple_notes
):
    bearer = get_token(client, "email1@example.com", "password")
    owner_user_id = await get_user_id_by_email("email1@example.com")
    headers = {"Authorization": f"Bearer {bearer}"}
    params = {"notes_user_id": f"{owner_user_id}"}
    response = client.get("/notes/", headers=headers, params=params)
    assert response.status_code == status.HTTP_200_OK
    resp_data = response.json()
    assert len(resp_data) == 2


async def test_authorized_as_simple_get_notes_another_owner(
    drop_mock_db, add_3_simple_users, add_3_simple_notes
):
    bearer = get_token(client, "email2@example.com", "password")
    owner_user_id = await get_user_id_by_email("email1@example.com")
    headers = {"Authorization": f"Bearer {bearer}"}
    params = {"notes_user_id": f"{owner_user_id}"}
    response = client.get("/notes/", headers=headers, params=params)
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_authorized_as_admin_get_note(
    drop_mock_db, add_3_simple_users, add_3_simple_notes
):
    bearer = get_token(client, "admin@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    note_id = await get_note_id_by_title("title 1")
    response = client.get(f"/notes/{note_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK


async def test_authorized_as_admin_put_note(drop_mock_db, add_3_simple_users):
    bearer = get_token(client, "admin@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    data = {"title": "title 1", "body": "body 1"}
    response = client.put("/notes/111111111111111111111111", headers=headers, json=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_authorized_as_admin_patch_note(drop_mock_db, add_3_simple_users):
    bearer = get_token(client, "admin@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    data = {"title": "title 1", "body": "body 1"}
    response = client.patch(
        "/notes/111111111111111111111111", headers=headers, json=data
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_authorized_as_admin_delete_note(drop_mock_db, add_3_simple_users):
    bearer = get_token(client, "admin@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    response = client.delete(f"/notes/111111111111111111111111", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_authorized_as_simple_user_restore_note_data(
    drop_mock_db, add_3_simple_users
):
    bearer = get_token(client, "email1@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    response = client.get(f"/notes/restore/111111111111111111111111", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_authorized_as_admin_get_note_restore_not_deleted_note_data(
    drop_mock_db, add_3_simple_users
):
    bearer = get_token(client, "admin@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    response = client.get(f"/notes/restore/111111111111111111111111", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_authorized_as_admin_get_note_restore_deleted_note_data(
    drop_mock_db, add_3_simple_users, add_3_simple_notes
):
    bearer = get_token(client, "email1@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}
    note_id = await get_note_id_by_title("title 1")
    response = client.delete(f"/notes/{note_id}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    bearer = get_token(client, "admin@example.com", "password")
    headers = {"Authorization": f"Bearer {bearer}"}

    response = client.get(f"/notes/restore/{note_id}", headers=headers)
    assert response.status_code == status.HTTP_201_CREATED

    response = client.get(f"/notes/{note_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
