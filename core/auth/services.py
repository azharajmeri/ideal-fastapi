from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from starlette.responses import Response

from core.auth.models import User
from core.auth.schemas import UserRegistrationRequestSchema
from core.auth.utils import Hasher
from core.constants import ERR_MSG_USER_ALREADY_EXIST
from core.exceptions import ExistsError
from core.utils import convert_data_into_json

_hasher = Hasher()


async def register(request: UserRegistrationRequestSchema, response: Response):
    """
    Register a new user.
    This function is used to register a new user in the application. It takes a `UserRegistrationRequest` instance
    as input, which contains the user's email and password. The function validates the input, creates a new user in
    the database, and returns a `UserRegistrationResponse` indicating the result of the registration.

    :param request: The user registration request data, including the email and password.
    :return: A response indicating the result of the user registration request.
    :raises: ValueError: If the email address or password is invalid.
             Exception: If an error occurs while creating the user in the database.
    """
    data, message = None, ""
    request_data = convert_data_into_json(request)
    email_filter_list = [User.email == request_data.get("email")]
    # if _ := db_interface.get_single_item_by_filters(email_filter_list):
    #     raise ExistsError(ERR_MSG_USER_ALREADY_EXIST)
    # request_data["password"] = _hasher.get_password_hash(request_data.get("password"))
    # data = db_interface.create_with_uuid(data=request_data)
    # message = "User Register Successfully."
    return {"message": message, "data": data}
