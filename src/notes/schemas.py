from typing import Optional

from pydantic import BaseModel, Field

from src.service import dict_fields_to_str_converter


class NoteBaseSchema(BaseModel):
    title: str = Field(..., max_length=256)
    body: Optional[str] = Field(None, max_length=65536)


class NoteUpdateSchema(NoteBaseSchema):
    title: Optional[str] = Field(None, max_length=256)


class NoteDBSchema(NoteBaseSchema):
    owner: str = Field(...)
