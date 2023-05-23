from serverhttpy.exceptions.invalid_header_structure import (
    InvalidHeaderStructureException,
)


class UnsupportedMethodSpecifiedException(InvalidHeaderStructureException):
    __BASE_MESSAGE = "Unsupported HTTP method used in request: {method}."

    def __init__(self, method: str):
        super().__init__(self.__BASE_MESSAGE.format(method=method))
