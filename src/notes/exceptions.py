from fastapi import HTTPException
from starlette import status


class HTTPNotesListEmpty(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Empty list returned",
        )


class HTTPNoteNoExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note no exists",
        )


class HTTPNoteDeleted(HTTPException):
    def __init__(self, id: str | None = None):
        super().__init__(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Note with id {id} deleted",
        )


class HTTPNoteAccessDenied(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Note access denied",
        )
