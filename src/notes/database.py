from bson import ObjectId

from src.database import db_note_collection, db_removed_note_collection
from src.service import dict_fields_to_str_converter


async def retrieve_notes(owner_id: str | None = None) -> list[dict]:
    """
    Retrieve all notes present in the database, if owner_id is None.
    In otherwise, retrieve all notes for a specific owner.
    """
    notes = []
    if owner_id:
        async for note in db_note_collection.find({"owner": owner_id}):
            notes.append(dict_fields_to_str_converter(note))
    else:
        async for note in db_note_collection.find():
            notes.append(dict_fields_to_str_converter(note))
    return notes


async def add_note_in_db(note_data: dict) -> dict:
    """
    Add a new note into the database
    """
    # If there is a "_id" field, then you should convert the ObjectId type
    # so that in the future there will be no problems with searching for folders by "_id"
    if "_id" in note_data:
        note_data["_id"] = ObjectId(note_data["_id"])

    note = await db_note_collection.insert_one(note_data)
    new_note = await retrieve_note(note.inserted_id)
    return dict_fields_to_str_converter(new_note)


async def retrieve_note(note_id: str) -> dict | None:
    """
    Retrieve a note with a matching ID
    """
    note = await db_note_collection.find_one({"_id": ObjectId(note_id)})
    if note:
        return dict_fields_to_str_converter(note)


async def update_note(note_id: str, data: dict) -> dict | None:
    """
    Update a note with a matching ID.
    Before calling, make sure the object exists!
    """
    updated_note = await db_note_collection.update_one(
        {"_id": ObjectId(note_id)}, {"$set": data}
    )
    if updated_note:
        return await retrieve_note(note_id)


async def delete_note(note_id: str) -> None:
    """
    Delete a note with a matching ID.
    Before calling, make sure the object exists!
    """
    await db_note_collection.delete_one({"_id": ObjectId(note_id)})


async def get_note_id_by_title(title: str) -> str:
    """
    Retrieve the note ID from the database by its title.
    """
    note = await db_note_collection.find_one({"title": title})
    if note:
        return str(note["_id"])


async def add_note_in_removed_db(note_data: dict) -> None:
    """
    Add a note into the database of removed notes
    """
    # Should convert the ObjectId type
    # so that in the future there will be no problems with searching for folders by "_id"
    note_data["_id"] = ObjectId(note_data["_id"])
    await db_removed_note_collection.insert_one(note_data)


async def pop_note_from_removed_db(note_id: str) -> dict | None:
    """
    Remove and retrieve a note from the database  of removed notes by its ID.
    """
    note = await retrieve_note_from_removed_db(note_id)
    if note:
        await delete_note_from_removed_db(note_id)
        return dict_fields_to_str_converter(note)


async def retrieve_note_from_removed_db(note_id: str) -> dict | None:
    """
    Retrieve a note from the database of removed notes by its ID.
    """
    note = await db_removed_note_collection.find_one({"_id": ObjectId(note_id)})
    if note:
        return dict_fields_to_str_converter(note)


async def delete_note_from_removed_db(note_id: str) -> None:
    """
    Delete a note from the database of removed notes by its ID.
    """
    await db_removed_note_collection.delete_one({"_id": ObjectId(note_id)})
