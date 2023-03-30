from typing import Dict, Any, Type

from pydantic import BaseModel
from starlette import status


class ResponseMessage(BaseModel):
    message: str


class AuthenticationResponseModel:

    def __init__(self):
        self.status_code_mapper = {
            'INTERNAL_SERVER_ERROR': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'BAD_REQUEST': status.HTTP_400_BAD_REQUEST,
            'FORBIDDEN': status.HTTP_403_FORBIDDEN,
            'UNAUTHORIZED': status.HTTP_401_UNAUTHORIZED,
            'RESPONSE_MODEL': {"model": ResponseMessage}
        }

    def common_response_messages(self) -> Dict[Any, Dict[str, Type[ResponseMessage]]]:
        """
        Returns a dictionary that maps any object to a dictionary of response messages.
        The second dictionary maps strings to `ResponseMessage` type objects, which represent the possible response messages.

        :return: Dict[Any, Dict[str, Type[ResponseMessage]]]: A dictionary that maps any object to a dictionary of response messages.
        """
        return {self.status_code_mapper.get('INTERNAL_SERVER_ERROR'): self.status_code_mapper.get('RESPONSE_MODEL'),
                self.status_code_mapper.get('BAD_REQUEST'): self.status_code_mapper.get('RESPONSE_MODEL')}

    def register_response_model(self):
        return self.common_response_messages()