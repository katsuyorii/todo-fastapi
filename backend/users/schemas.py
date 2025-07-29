from pydantic import BaseModel, EmailStr, Field

from datetime import datetime, date


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: str
    date_of_birth: date | None
    is_active: bool
    is_mailing: bool
    created_at: datetime
    updated_at: datetime


class UserUpdateSchema(BaseModel):
    username: str | None = Field(default=None)
    date_of_birth: date | None = Field(default=None)
    is_mailing: bool | None = Field(default=None)
