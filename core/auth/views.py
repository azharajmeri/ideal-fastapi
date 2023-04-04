from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from core.auth.schemas import UserRegistrationRequestSchema, UserRegistrationResponse, UserLoginResponse, \
    UserLoginRequest
from core.auth.services import register, login
from core.constants import REGISTER_SUMMARY, LOGIN_SUMMARY
from core.database.core import get_db
from core.response_models.auth_response_model import AuthenticationResponseModel

auth_router = APIRouter(
    tags=["Authentication"],
)
user_router = APIRouter(
    tags=["User"],
)

_auth_response_model = AuthenticationResponseModel()


@auth_router.post("/api/register", status_code=status.HTTP_201_CREATED, response_model=UserRegistrationResponse,
                  summary=REGISTER_SUMMARY,
                  responses=_auth_response_model.register_response_model())
async def register_user(request: UserRegistrationRequestSchema, session: Session = Depends(get_db)):
    """
    Endpoint for user registration.
    This endpoint is responsible for registering new users in the application.

    Parameters:

        request :
            The incoming request object containing the user's registration data.
        session : Session
            A SQLAlchemy Session object used to interact with the database.

    Raises:

        HTTPException :
            If any required fields are missing from the request or if the provided
                email address is already in use.

    Returns:

        JSON response indicating the success or failure of the registration process.
    """
    return await(register(request, session))


@auth_router.post("/api/login", status_code=status.HTTP_200_OK, response_model=UserLoginResponse,
                  summary=LOGIN_SUMMARY, responses=_auth_response_model.login_response_model())
def api_user_login(request: UserLoginRequest, session: Session = Depends(get_db)):
    """
    Endpoint for user login.
    This endpoint is responsible for handling user authentication and returning a JSON Web Token (JWT) on successful login.

    Parameters:

        request :
            The incoming request object containing the user's email and password.
        session : Session
            A SQLAlchemy Session object used to interact with the database.

    Returns:

        JSON response containing the JWT if the user's credentials are valid, or a JSON error response if authentication fails.

    Raises:

         HTTPException :
            If any required fields are missing from the request or if the provided email and password do not match any existing user account.
    """
    return login(request, session)
