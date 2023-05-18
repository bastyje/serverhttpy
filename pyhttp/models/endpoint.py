from typing import Callable

from pyhttp.enums.http_method import HTTPMethod
from pyhttp.exceptions.no_action_registered_in_endpoint import NoActionRegisteredInEndpointException
from pyhttp.models.path import Path
from pyhttp.models.request import Request
from pyhttp.models.response import Response


class Endpoint:
    path: Path
    http_method: HTTPMethod
    action: Callable[[Request], Response]

    def __init__(self, path: Path, http_method: HTTPMethod, action: Callable[[Request], Response] = None):
        self.path = path
        self.http_method = http_method
        self.action = action

    def __eq__(self, other):
        return isinstance(other, Endpoint) and self.path == other.path and self.http_method == other.http_method

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return f'{self.http_method} {self.path}'

    def execute(self, request: Request):
        if self.action is None:
            raise NoActionRegisteredInEndpointException(repr(Endpoint))
        return self.action(request)
