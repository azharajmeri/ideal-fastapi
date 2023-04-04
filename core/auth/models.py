from sqlalchemy import Boolean, Column, String

from core.database.core import Base
from core.database.manager import QueryManager
from core.models import TimeStampMixin


class User(Base, TimeStampMixin, QueryManager):
    """
    Model for storing user information.

    This model is used to store information about users in the application, including their
    firstname, lastname, email, password hash, and other relevant information.

    Fields:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user. Must be a valid email address format.
        password_hash (str): The hashed password of the user.
        is_active (bool): Indicates whether the user is active or inactive.
        created_at (datetime): The timestamp for when the user was created.
        updated_at (datetime): The timestamp for when the user was last updated.
    """
    __tablename__ = "user"
    id = Column(String(255), primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    is_active = Column(Boolean, default=True)
