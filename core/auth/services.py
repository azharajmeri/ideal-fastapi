from sqlalchemy.orm import Session

from core.auth.models import User
from core.auth.schemas import UserRegistrationRequestSchema, UserLoginRequest, UserVerifyOTPRequest
from core.auth.utils import Hasher, JWTAuthenticator, verify_otp, urlsafe_base64_decode, generate_otp, \
    urlsafe_base64_encode
from core.constants import ERR_MSG_USER_ALREADY_EXIST, USER_REGISTRATION_SUCCESS, ERR_EMAIL_INCORRECT, \
    ERR_PASSWORD_INCORRECT, USER_LOGIN_SUCCESS, USER_OTP_VERIFICATION_FAILED, USER_OTP_VERIFICATION_SUCCESS
from core.exceptions import ExistsError, BadRequestException
from core.utils import convert_data_into_json

_hasher = Hasher()
jwt_authentication = JWTAuthenticator()


async def register(request: UserRegistrationRequestSchema, session: Session):
    """
    Register a new user.
    This function is used to register a new user in the application. It takes a `UserRegistrationRequest` instance
    as input, which contains the user's email and password. The function validates the input, creates a new user in
    the database, and returns a `UserRegistrationResponse` indicating the result of the registration.

    Parameters:
        request : The user registration request data, including the email and password.
        session : Session
            A SQLAlchemy Session object used to interact with the database.

    Returns:
        A response indicating the result of the user registration request.

    Raises:
        ValueError : If the email address or password is invalid.
        ExistsError : User with the given email already exists.
    """
    request_data = convert_data_into_json(request)
    if _ := User.get_single_item_by_filters([User.email == request_data.get("email")], session):
        raise ExistsError(ERR_MSG_USER_ALREADY_EXIST)

    request_data["password"] = _hasher.get_password_hash(request_data.get("password"))
    data = User.create_with_uuid(data=request_data, session=session)
    print(urlsafe_base64_encode(str(data.id).encode('utf-8')))
    print(generate_otp(data.id))
    return {"message": USER_REGISTRATION_SUCCESS, "data": data}


def login(request: UserLoginRequest, session: Session):
    """
    Login an existing user.
    This function is used to log in an existing user in the application. It takes a `UserLoginRequest` instance as
    input, which contains the user's email and password. The function validates the input, checks the user's
    credentials against the database, and returns a `UserLoginResponse` indicating the result of the login.

    Parameters:
        request : The user OTP verification request data, including the UID and OTP.

    Returns:
        A response indicating the result of the user login request.

    Raises:
        ValueError : If the email address or password is invalid.
        BadRequestException : if the email or password are not as per the requirement.
    """
    request_data = convert_data_into_json(request)
    if not (user_object := User.get_single_item_by_filters([User.email == request_data.get("email")], session)):
        raise BadRequestException(ERR_EMAIL_INCORRECT)
    if not _hasher.verify_password(request_data.get("password"), user_object.password):
        raise BadRequestException(ERR_PASSWORD_INCORRECT)
    access_token = jwt_authentication.create_access_token(payload={"sub": user_object.email})
    refresh_token = jwt_authentication.create_refresh_token(payload={"sub": user_object.email})
    data = {"access_token": access_token, "refresh_token": refresh_token}
    return {"message": USER_LOGIN_SUCCESS, "data": data}


def verify_otp_service(request: UserVerifyOTPRequest, session: Session):
    """
    Login an existing user.
    This function is used to log in an existing user in the application. It takes a `UserLoginRequest` instance as
    input, which contains the user's email and password. The function validates the input, checks the user's
    credentials against the database, and returns a `UserLoginResponse` indicating the result of the login.

    Parameters:
        request : The user OTP verification request data, including the UID and OTP.

    Returns:
        A response indicating the result of the user login request.

    Raises:
        ValueError : If the email address or password is invalid.
        BadRequestException : if the email or password are not as per the requirement.
    """
    request_data = convert_data_into_json(request)
    encoded_uid = request_data.get("uid")
    otp = request_data.get("otp")
    if not verify_otp(urlsafe_base64_decode(encoded_uid).decode('utf-8'), otp):
        return {"message": USER_OTP_VERIFICATION_FAILED}
    return {"message": USER_OTP_VERIFICATION_SUCCESS}
