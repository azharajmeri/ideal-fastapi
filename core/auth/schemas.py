from typing import Union

from pydantic import BaseModel, Field, EmailStr

from core.constants import PASSWORD_REGEX
from core.response_models.auth_response_model import ResponseMessage


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


class UserRegistrationResponseData(BaseModel):
    """
    Response schema for user registration.
    """
    id: str
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class UserRegistrationResponse(ResponseMessage):
    data: Union[UserRegistrationResponseData, None]
