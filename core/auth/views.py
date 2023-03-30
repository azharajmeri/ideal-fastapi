from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from core.auth.schemas import UserRegistrationRequestSchema
from core.auth.services import register
from core.constants import REGISTER_SUMMARY
from core.response_models.auth_response_model import AuthenticationResponseModel

auth_router = APIRouter(
    tags=["Authentication"],
)
user_router = APIRouter(
    tags=["User"],
)

_auth_response_model = AuthenticationResponseModel()


@auth_router.post("/api/register", status_code=status.HTTP_201_CREATED, response_model=AuthenticationResponseModel,
             summary=REGISTER_SUMMARY,
             responses=_auth_response_model.register_response_model())
async def register_user(request: UserRegistrationRequestSchema, response: Response):
    """
    Endpoint for user registration.
    This endpoint is responsible for registering new users in the application.

    :param request: The incoming request object containing the user's registration data.
    :return: JSON response indicating the success or failure of the registration process.
    :raises HTTPException: If any required fields are missing from the request or if the provided email address is already in use.
    """
    return await(register(request, response))