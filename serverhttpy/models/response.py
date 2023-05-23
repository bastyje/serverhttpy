from serverhttpy.enums.status_code import StatusCode
from serverhttpy import supported_protocol


class Response:
    status_code: StatusCode
    protocol: str
    headers: dict
    body: str

    def __str__(self):
        return (
            f"{self.protocol} {self.status_code.value} {self.status_code.description()}"
        )

    def __repr__(self):
        base = self.__str__()

        if self.headers is not None:
            for index, header in enumerate(self.headers):
                if index == 0:
                    base += "\n"
                base += f"{header}: {self.headers[header]}"
                if index <= len(self.headers) - 1:
                    base += "\n"

        if self.body is not None and len(self.body) > 0:
            base += "\n"
            base += self.body

        return base

    def __init__(self, status_code: StatusCode, headers: dict = None, body: str = None):
        self.status_code = status_code
        self.protocol = supported_protocol
        self.headers = headers
        self.body = body
