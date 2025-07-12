from pydantic import BaseModel, EmailStr, Field


class UserRegistrationSchema(BaseModel):
    username: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    password: str