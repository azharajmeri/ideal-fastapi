from pydantic import BaseModel, Field, EmailStr

from core.constants import PASSWORD_REGEX


class UserRegistrationRequestSchema(BaseModel):
    """
    Request schema for user registration.
    """
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    password: str = Field(regex=PASSWORD_REGEX)
    email: EmailStr

    class Config:
        extra = "forbid"
