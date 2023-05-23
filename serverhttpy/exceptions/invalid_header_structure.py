from serverhttpy.exceptions.invalid_request_structure import (
    InvalidRequestStructureException,
)


class InvalidHeaderStructureException(InvalidRequestStructureException):
    __BASE_MESSAGE = "HTTP request header has invalid format.\n{message}"

    def __init__(self, message):
        super().__init__(self.__BASE_MESSAGE.format(message=message))
