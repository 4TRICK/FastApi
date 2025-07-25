import motor.motor_asyncio
from mongomock_motor import AsyncMongoMockClient

from src.settings import get_settings

is_mock = False

if get_settings().testing:
    client = AsyncMongoMockClient()
    is_mock = True
else:
    client = motor.motor_asyncio.AsyncIOMotorClient(get_settings().get_mongo_detail())
    is_mock = False
db_note_collection = client.dbNotes.get_collection(
    f"{get_settings().mongo_db_note_coll}_collection"
)

db_removed_note_collection = client.dbNotes.get_collection(
    f"{get_settings().mongo_db_removed_note_coll}_collection"
)

db_auth_collection = client.dbNotes.get_collection(
    f"{get_settings().mongo_db_auth_coll}_collection"
)


async def drop_collections():
    await db_note_collection.drop()
    await db_removed_note_collection.drop()
    await db_auth_collection.drop()


# def init_db(app: FastAPI):
#     """
#     Initialise db connection at startup
#     Shutdown the db at shutdown
#     :param app: FastAPI to initialise
#     :return: None
#     """
#
#     @app.on_event("startup")
#     async def startup_db_client():
#         if TESTING:
#             client = AsyncMongoMockClient()
#         else:
#             client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
#
#         app.mongodb_client = client
#         app.db_note_collection = client.dbNotes.get_collection(f"{MONGO_DB_NOTE_COLLECTION}_collection")
#         app.db_auth_collection = client.dbNotes.get_collection(f"{MONGO_DB_AUTH_COLLECTION}_collection")
#
#     @app.on_event("shutdown")
#     async def shutdown_db_client():
#         app.mongodb_client.close()
