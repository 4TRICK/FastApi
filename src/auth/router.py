import logging
from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from src.auth.database import add_user_in_db, retrieve_user_by_email
from src.auth.dependencies import CurrentActiveUser
from src.auth.exceptions import HTTPIncorrectUsernameOrPassword, HTTPUserAlreadyExists
from src.auth.schemas import Token, UserAuthSchema, UserSchema
from src.auth.service import authenticate_user, create_access_token, get_password_hash
from src.service import dict_fields_to_str_converter
from src.settings import get_settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register", response_description="User registered")
async def register(user_data: UserSchema = Body(...)):
    """
    Register a new user.
    """
    logger.info("Registering user: %s", user_data.email)

    if not await retrieve_user_by_email(user_data.email):
        user_data.password = get_password_hash(user_data.password)
        new_user = await add_user_in_db(jsonable_encoder(user_data))
        if new_user:
            return JSONResponse(
                dict_fields_to_str_converter(new_user),
                status_code=status.HTTP_201_CREATED,
            )
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        raise HTTPUserAlreadyExists(user_data.email)


@router.post("/token", response_description="User authenticated")
async def token(user_data: UserAuthSchema = Body(...)):
    """
    Authenticate a user and return an access token.
    """
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    if not user:
        raise HTTPIncorrectUsernameOrPassword()
    access_token_expires = timedelta(minutes=get_settings().access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/user", response_description="Current user info")
async def user_info(current_user: CurrentActiveUser):
    """
    Get current user info.
    """
    return {"email": current_user["email"]}
