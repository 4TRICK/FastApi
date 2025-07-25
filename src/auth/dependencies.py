from typing import Annotated

from fastapi import Depends

from src.auth.schemas import UserSchema
from src.auth.service import get_current_user


async def get_current_active_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    return current_user


CurrentActiveUser = Annotated[UserSchema, Depends(get_current_active_user)]
