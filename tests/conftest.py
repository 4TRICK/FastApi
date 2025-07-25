import asyncio

import pytest

from src.auth.database import add_user_in_db, get_user_id_by_email
from src.auth.service import get_password_hash
from src.database import drop_collections, is_mock
from src.notes.database import add_note_in_db


@pytest.fixture(scope="function")
def drop_mock_db():
    if is_mock:
        asyncio.run(drop_collections())
    else:
        raise NotImplementedError("This test only applies to mock DB")


@pytest.fixture(scope="function")
def add_simple_user():
    asyncio.run(
        add_user_in_db(
            {
                "email": "email@example.com",
                "password": get_password_hash("password"),
                "is_admin": False,
            }
        )
    )


@pytest.fixture(scope="function")
def add_3_simple_users():
    async def add_users():
        await add_user_in_db(
            {
                "email": "email1@example.com",
                "password": get_password_hash("password"),
                "is_admin": False,
            }
        )

        await add_user_in_db(
            {
                "email": "email2@example.com",
                "password": get_password_hash("password"),
                "is_admin": False,
            }
        )

        await add_user_in_db(
            {
                "email": "email3@example.com",
                "password": get_password_hash("password"),
                "is_admin": False,
            }
        )

        await add_user_in_db(
            {
                "email": "admin@example.com",
                "password": get_password_hash("password"),
                "is_admin": True,
            }
        )

    asyncio.run(add_users())


@pytest.fixture(scope="function")
def add_simple_note():
    async def add_note():
        user_id = await get_user_id_by_email("email@example.com")
        await add_note_in_db({"title": "title 1", "body": "body 1", "owner": user_id})

    asyncio.run(add_note())


@pytest.fixture(scope="function")
def add_3_simple_notes():
    async def add_notes():
        user_id = await get_user_id_by_email("email1@example.com")
        await add_note_in_db({"title": "title 1", "body": "body 1", "owner": user_id})
        await add_note_in_db({"title": "title 2", "body": "body 2", "owner": user_id})

        user_id = await get_user_id_by_email("email2@example.com")
        await add_note_in_db({"title": "title 3", "body": "body 3", "owner": user_id})

    asyncio.run(add_notes())


def get_token(client, email, password):
    data = {"email": email, "password": password}
    response = client.post("/auth/token", json=data)
    resp_data = response.json()
    return resp_data["access_token"]
