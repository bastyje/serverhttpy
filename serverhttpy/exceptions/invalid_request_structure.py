class InvalidRequestStructureException(Exception):
    __BASE_MESSAGE = "HTTP request has invalid structure:\n{message}"

    def __init__(self, message):
        super().__init__(self.__BASE_MESSAGE.format(message=message))
