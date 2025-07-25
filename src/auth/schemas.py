from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    is_admin: Optional[bool] = Field(default=False)


class UserAuthSchema(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(...)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
