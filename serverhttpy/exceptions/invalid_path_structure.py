from serverhttpy.exceptions.invalid_header_structure import (
    InvalidHeaderStructureException,
)


class InvalidPathStructureException(InvalidHeaderStructureException):
    __BASE_MESSAGE = "HTTP request path has invalid format.\n{message}"

    def __init__(self, message):
        super().__init__(self.__BASE_MESSAGE.format(message=message))
