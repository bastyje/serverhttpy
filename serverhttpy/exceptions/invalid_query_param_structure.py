from serverhttpy.exceptions.invalid_path_structure import InvalidPathStructureException


class InvalidQueryParamStructureException(InvalidPathStructureException):
    __BASE_MESSAGE = "HTTP request query parameter has invalid format.\n{message}"

    def __init__(self, message):
        super().__init__(self.__BASE_MESSAGE.format(message=message))
