from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.logger import logger, log_middleware
from src.notes.router import router as notes_router

description = """
NoteFastAPI will help you not to forget anything!

## Notes

If you simple user you can:
* Create a new note.
* View all own notes.
* View specific own note.
* Update own notes.
* Delete own notes.

If you administrator you can:
* View all notes.
* View all notes by a specific user.
* View specific note.
* Restore deleted notes.

## Auth

You can:

* Create simple user or administrator.
* Login with registered user.
"""

app = FastAPI(
    title="NotesFastApi",
    description=description,
    docs_url="/api/docs",
    openapi_url="/api",
    contact={"name": "Churilov Evgeny", "email": "i@churilovevgeny.ru"},
)
app.include_router(notes_router)
app.include_router(auth_router)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)


@app.get("/")
async def root():
    return {"message": f"Welcome to NotesFastAPI!"}


@app.on_event("startup")
def on_startup():
    logger.info("Starting application...")


@app.on_event("shutdown")
def on_shutdown():
    logger.info("Stopping application...")
