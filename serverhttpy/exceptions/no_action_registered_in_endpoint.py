class NoActionRegisteredInEndpointException(Exception):
    __BASE_MESSAGE: str = "There is no action defined for endpoint {endpoint}."

    def __init__(self, endpoint: str):
        super().__init__(self.__BASE_MESSAGE.format(endpoint=endpoint))
