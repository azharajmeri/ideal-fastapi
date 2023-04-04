from datetime import timedelta, datetime, timezone

from jose import jwt
from passlib.context import CryptContext
from starlette import status
from starlette.exceptions import HTTPException

from core.config import app_config


class Hasher:
    """
    Hasher is a class that provides methods for hashing and verifying passwords.
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        Verify if the given plain password matches the given hashed password.

        :param plain_password: The plain password to verify.
        :param hashed_password: The hashed password to compare against.
        :return: True if the passwords match, False otherwise.
        """
        return Hasher.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        """
        This function generates a hash for the given password using a strong bcrypt hash function.
        :param password: A string representing the plain password to be hashed.
        :return: A string representing the hashed password.
        """
        return Hasher.pwd_context.hash(password)


class JWTAuthenticator:
    """
    The JWTAuthenticator class provides functionality for authenticating user requests by verifying JWT tokens in the
    Authorization header.
    """

    def __init__(self, ):
        self.ALGORITHM = app_config.JWT_ALGORITHM

    def create_token(self, payload: dict, secret_key: str, expires_delta: timedelta):
        """
        Create a JSON Web Token (JWT) based on the given payload, secret key, and expiration time delta.

        :param payload: A dictionary containing the data to be encoded in the JWT.
        :param secret_key: The secret key to be used for encoding the JWT.
        :param expires_delta: The time delta for when the JWT should expire.
        :return: A JSON Web Token (JWT) string.
        """
        payload["exp"] = datetime.now(timezone.utc) + expires_delta
        return jwt.encode(payload, secret_key,
                          algorithm=self.ALGORITHM, )

    def decode_token(self, token: str, secret_key: str):
        """
        Decode a JWT token and return its payload.

        :param token: The JWT token to be decoded.
        :param secret_key: The secret key used for encoding the token.
        :return: The payload contained in the token.
        :raises: jwt.exceptions.InvalidSignatureError: If the signature of the token is invalid
                 jwt.exceptions.DecodeError: If the token is invalid or expired.
        """
        payload = jwt.decode(token, secret_key, algorithms=[self.ALGORITHM])
        sub_data: str = payload.get("sub")
        if sub_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return sub_data

    def create_access_token(self, payload: dict):
        """
        Create a JWT access token.

        :param payload: A dictionary containing the payload data to be encoded in the JWT token.
        :return: A JWT access token.
        :raises: Exception: If an error occurs during the encoding process.
        """
        access_token_expires = timedelta(minutes=app_config.ACCESS_TOKEN_EXPIRE_MINUTES)
        return self.create_token(payload=payload, secret_key=app_config.ACCESS_TOKEN_SECRET_KEY,
                                 expires_delta=access_token_expires)

    def create_refresh_token(self, payload: dict):
        """
        Create and return a refresh token.

        :param payload: The data to be encoded and stored in the token.
        :return: The created refresh token.
        :raises: Exception: If an error occurs during the encoding process.
        """
        refresh_token_expires = timedelta(minutes=app_config.REFRESH_TOKEN_EXPIRE_MINUTES)
        return self.create_token(payload=payload, secret_key=app_config.REFRESH_TOKEN_SECRET_KEY,
                                 expires_delta=refresh_token_expires)
