from pydantic.errors import PydanticValueError


class BadRequestException(Exception):
    def __init__(self, msg):
        self.msg = msg


class ExistsError(Exception):
    def __init__(self, msg):
        self.msg = msg


class NotFoundError(Exception):
    def __init__(self, msg):
        self.msg = msg
