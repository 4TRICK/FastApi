from src.database import db_auth_collection


async def add_user_in_db(user_data: dict) -> dict:
    """
    Add a new user to the database.
    """
    user = await db_auth_collection.insert_one(user_data)
    return await retrieve_user_by_id(user.inserted_id)


async def retrieve_user_by_email(user_email: str) -> dict:
    """
    Retrieve a user by their email.
    """
    return await db_auth_collection.find_one({"email": user_email})


async def retrieve_user_by_id(user_id: str) -> dict:
    """
    Retrieve a user by their ID.
    """
    return await db_auth_collection.find_one({"_id": user_id})


async def get_user_id_by_email(email: str) -> str:
    """
    Retrieve the user ID by their email.
    """
    user = await retrieve_user_by_email(email)
    return str(user["_id"]) if user else None
