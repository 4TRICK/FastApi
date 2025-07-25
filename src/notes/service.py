from src.notes.schemas import NoteBaseSchema, NoteDBSchema


async def get_user_id_from_current_user(current_user) -> str:
    """
    Extract and return the user ID from the current user.
    """
    return str(current_user["_id"])


async def is_user_admin(current_user) -> bool:
    """
    Check if the current user is an admin.
    """
    return current_user["is_admin"]


async def get_note_db_schema_object(current_user, note: NoteBaseSchema) -> NoteDBSchema:
    """
    Create a NoteDBSchema object from the given NoteBaseSchema object and current user.
    """
    user_id = await get_user_id_from_current_user(current_user)
    return NoteDBSchema(title=note.title, body=note.body, owner=user_id)
