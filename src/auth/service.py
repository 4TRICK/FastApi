from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext
from pydantic import EmailStr

from src.auth.database import retrieve_user_by_email
from src.auth.exceptions import HTTPCredentialsException
from src.auth.schemas import TokenData
from src.settings import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode, get_settings().secret_key, get_settings().algorithm
    )
    return encode_jwt


def get_password_hash(password: str) -> str:
    """
    Hash a plain password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Extract and return the user from the access token.
    """
    try:
        payload = jwt.decode(
            token, get_settings().secret_key, algorithms=[get_settings().algorithm]
        )
        email: str = payload.get("sub")
        if email is None:
            raise HTTPCredentialsException()
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise HTTPCredentialsException()
    except JWTError:
        raise HTTPCredentialsException()
    user = await retrieve_user_by_email(token_data.email)
    if user is None:
        raise HTTPCredentialsException()
    return user


async def authenticate_user(email: EmailStr, password: str):
    """
    Authenticate a user and return the user object if the credentials are valid.
    """
    user = await retrieve_user_by_email(email)
    if user and verify_password(
        plain_password=password, hashed_password=user["password"]
    ):
        return user
