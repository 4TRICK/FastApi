from fastapi import HTTPException
from starlette import status


class HTTPUserAlreadyExists(HTTPException):
    def __init__(self, email: str | None = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Users with email {email} already exist.",
        )


class HTTPIncorrectUsernameOrPassword(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


class HTTPCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
