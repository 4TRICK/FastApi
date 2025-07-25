from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from src.auth.dependencies import CurrentActiveUser
from src.notes.database import (
    add_note_in_db,
    add_note_in_removed_db,
    delete_note,
    pop_note_from_removed_db,
    retrieve_note,
    retrieve_notes,
    update_note,
)
from src.notes.exceptions import (
    HTTPNoteAccessDenied,
    HTTPNoteDeleted,
    HTTPNoteNoExists,
    HTTPNotesListEmpty,
)
from src.notes.schemas import NoteBaseSchema, NoteUpdateSchema
from src.notes.service import (
    get_note_db_schema_object,
    get_user_id_from_current_user,
    is_user_admin,
)
from src.service import dict_fields_to_str_converter, list_fields_to_str_converter

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.post("/", response_description="Note data added into the database")
async def create_note(
    note: NoteBaseSchema,
    current_user: CurrentActiveUser,
):
    """
    Create a new note in the database.
    If current user is administrator, then raise HTTPNoteAccessDenied.
    """
    if await is_user_admin(current_user):
        raise HTTPNoteAccessDenied()

    db_note = await get_note_db_schema_object(current_user, note)
    new_note = await add_note_in_db(jsonable_encoder(db_note))
    if new_note:
        return JSONResponse(
            dict_fields_to_str_converter(new_note),
            status_code=status.HTTP_201_CREATED,
        )
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/", response_description="Notes retrieved")
async def get_notes(current_user: CurrentActiveUser, notes_user_id: str | None = None):
    """
    Retrieves a list of notes.
    If notes_user_id is None, then return notes for current user if simple user authenticated or
    for all users if admin authenticated.
    If notes_user_id is not None, then return notes for notes_user_id user if admin authenticated or
    if user with notes_user_id now authenticated.
    """
    owner_id = None
    is_admin = await is_user_admin(current_user)

    if is_admin:
        owner_id = notes_user_id

    if not is_admin:
        owner_id = await get_user_id_from_current_user(current_user)

    if not is_admin and notes_user_id and notes_user_id != owner_id:
        raise HTTPNoteAccessDenied()

    notes = await retrieve_notes(owner_id)
    if notes:
        return JSONResponse(
            list_fields_to_str_converter(notes),
            status_code=status.HTTP_200_OK,
        )
    raise HTTPNotesListEmpty()


@router.get("/{note_id}", response_description="Note retrieved")
async def get_note(note_id: str, current_user: CurrentActiveUser):
    """
    Retrieve a note by ID.
    If note owner is not current user or current user not is administrator, then raise HTTPNoteAccessDenied.
    If note not exists, then raise HTTPNoteNoExists.
    """
    note = await retrieve_note(note_id)
    if note:
        if not await is_user_admin(current_user):
            owner_id = await get_user_id_from_current_user(current_user)
            if note["owner"] != owner_id:
                raise HTTPNoteAccessDenied()

        return JSONResponse(
            dict_fields_to_str_converter(note),
            status_code=status.HTTP_200_OK,
        )
    raise HTTPNoteNoExists()


@router.put("/{note_id}", response_description="Note updated")
async def update_student_data(
    note_id: str,
    req: NoteUpdateSchema,
    current_user: CurrentActiveUser,
):
    """
    Update (put) a note by ID.
    If note owner is not current user or current user is administrator, then raise HTTPNoteAccessDenied.
    If note not exists, then raise HTTPNoteNoExists.
    """
    if await is_user_admin(current_user):
        raise HTTPNoteAccessDenied()

    owner_id = await get_user_id_from_current_user(current_user)
    return await update_note_data_internal(note_id, owner_id, req)


@router.patch("/{note_id}", response_description="Note updated")
async def update_note_partially(
    note_id: str, req: NoteUpdateSchema, current_user: CurrentActiveUser
):
    """
    Update (patch) a note by ID.
    If note owner is not current user or current user is administrator, then raise HTTPNoteAccessDenied.
    If note not exists, then raise HTTPNoteNoExists.
    """
    if await is_user_admin(current_user):
        raise HTTPNoteAccessDenied()

    owner_id = await get_user_id_from_current_user(current_user)
    return await update_note_data_internal(note_id, owner_id, req)


async def update_note_data_internal(
    note_id: str, owner_id: str, data: NoteUpdateSchema
):
    data = {k: v for k, v in data.dict().items() if v is not None}
    if len(data) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    note = await retrieve_note(note_id)
    if note:
        if note["owner"] != owner_id:
            raise HTTPNoteAccessDenied()

        updated_note = await update_note(note_id, data)
        if updated_note:
            return JSONResponse(
                dict_fields_to_str_converter(updated_note),
                status_code=status.HTTP_200_OK,
            )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    raise HTTPNoteNoExists()


@router.delete("/{note_id}", response_description="Note deleted")
async def delete_note_data(note_id: str, current_user: CurrentActiveUser):
    """
    Delete a note by ID.
    If note owner is not current user or current user is administrator, then raise HTTPNoteAccessDenied.
    If note not exists, then raise HTTPNoteNoExists.
    """
    if await is_user_admin(current_user):
        raise HTTPNoteAccessDenied()

    note = await retrieve_note(note_id)
    if note:
        owner_id = await get_user_id_from_current_user(current_user)
        if note["owner"] != owner_id:
            raise HTTPNoteAccessDenied()

        await add_note_in_removed_db(note)
        await delete_note(note_id)

        raise HTTPNoteDeleted()

    raise HTTPNoteNoExists()


@router.get("/restore/{note_id}", response_description="Note restored")
async def restore_note_data(note_id: str, current_user: CurrentActiveUser):
    """
    Restore note by ID.
    If current user is not administrator, then raise HTTPNoteAccessDenied.
    If note not was deleted before, then raise HTTPNoteNoExists.
    """
    if not await is_user_admin(current_user):
        raise HTTPNoteAccessDenied()

    note = await pop_note_from_removed_db(note_id)
    if note:
        new_note = await add_note_in_db(note)
        if new_note:
            return JSONResponse(
                dict_fields_to_str_converter(new_note),
                status_code=status.HTTP_201_CREATED,
            )
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    raise HTTPNoteNoExists()
