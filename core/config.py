import os
from functools import lru_cache

from pydantic import BaseModel
from pydantic import BaseSettings


class ServerType(BaseModel):
    PRODUCTION: str = "production"
    DEVELOPMENT: str = "development"
    LOCAL: str = "local"


_app_server_type = ServerType()


class Config(BaseSettings):
    """
    Set base configuration, env variable configuration and server configuration.
    """
    HOST_URL: str
    HOST_PORT: int
    FASTAPI_LOG_LEVEL: str
    DATABASE_URL: str

    ACCESS_TOKEN_SECRET_KEY: str
    REFRESH_TOKEN_SECRET_KEY: str
    FORGOT_PASSWORD_TOKEN_SECRET_KEY: str
    JWT_ALGORITHM: str
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    FORGOT_PASSWORD_EXPIRE_MINUTES: int

    class Config:
        env_nested_delimiter = '__'
        env_file = ".env"
        env_file_encoding = "utf-8"

    """ The starting execution point of the app."""
    FASTAPI_APP = "main:app"
    FASTAPI_APP_RELOAD = True

    DEBUG: bool = False
    TESTING: bool = False


class LocalConfig(Config):
    """
    This class used to generate the config for the development instance.
    """
    DEBUG: bool = True
    TESTING: bool = True


class DevelopmentConfig(Config):
    """
    This class used to generate the config for the development instance.
    """
    DEBUG: bool = True
    TESTING: bool = True


class ProductionConfig(Config):
    """
    This class used to generate the config for the production instance.
    """


@lru_cache
def get_current_server_config():
    """
    This will check FASTAPI_ENV variable and create an object of configuration according to that.
    :return: Production or Development Config object.
    """
    server_type = os.getenv("ENV_FASTAPI_SERVER_TYPE", _app_server_type.LOCAL)
    if server_type == _app_server_type.DEVELOPMENT:
        return DevelopmentConfig()
    elif server_type == _app_server_type.PRODUCTION:
        return ProductionConfig()
    return LocalConfig()


app_config = get_current_server_config()
