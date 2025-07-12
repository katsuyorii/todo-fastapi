from pydantic import BaseModel, EmailStr, Field, field_validator

from core.validators.password import validator_password_complexity


class UserRegistrationSchema(BaseModel):
    username: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        return validator_password_complexity(value)