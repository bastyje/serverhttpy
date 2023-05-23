from serverhttpy.enums.http_method import HTTPMethod
from serverhttpy.exceptions.invalid_header_structure import (
    InvalidHeaderStructureException,
)
from serverhttpy.exceptions.unsupported_method_specified import (
    UnsupportedMethodSpecifiedException,
)
from serverhttpy.models.uri import URI


class Request:
    method: HTTPMethod
    protocol: str
    headers: dict
    uri: URI
    body: str
    request_arguments: dict

    def __str__(self):
        return f"{self.method.value} {self.uri} {self.protocol}"

    def __init__(self, request_string: str):
        request_lines = request_string.splitlines()

        if len(request_lines) == 0:
            raise InvalidHeaderStructureException("Header does not exist")

        header_row = request_lines[0]
        header_row_words = header_row.split(" ")

        if len(header_row_words) != 3:
            raise InvalidHeaderStructureException(header_row)

        try:
            self.method = HTTPMethod(header_row_words[0])
        except ValueError:
            raise UnsupportedMethodSpecifiedException(header_row_words[0])

        self.uri = URI(header_row_words[1])
        self.protocol = header_row_words[2]

        self.headers = dict()
        index = 1
        for index in range(1, len(request_lines)):
            if request_lines[index] == "":
                break

            header = request_lines[index].split(": ")

            if len(header) != 2:
                raise InvalidHeaderStructureException(header)

            self.headers[header[0]] = header[1]

        self.body = ""
        for body_index in range(index + 1, len(request_lines)):
            self.body += request_lines[body_index]
            if body_index < len(request_lines) - 1:
                self.body += "\n"
