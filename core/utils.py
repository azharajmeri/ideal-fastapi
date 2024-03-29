from typing import Dict, Any

from fastapi.encoders import jsonable_encoder

from core.database.core import Base


def convert_data_into_json(request_data):
    """
    convert_data_into_json is a function that converts the request data into a JSON object.

    :param request_data: Request data to be converted into a JSON object.
    :return: dict: The converted JSON object.
    """
    return jsonable_encoder(request_data)


def to_dict(obj: Base) -> Dict[str, Any]:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
