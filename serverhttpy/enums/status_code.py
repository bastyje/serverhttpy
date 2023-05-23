from enum import Enum


class StatusCode(Enum):
    OK = 200
    BadRequest = 400
    NotFound = 404
    MethodNotAllowed = 405
    InternalServerError = 500
    NotImplemented = 501

    def description(self):
        return {
            StatusCode.OK: "OK",
            StatusCode.BadRequest: "Bad Request",
            StatusCode.NotFound: "Not Found",
            StatusCode.MethodNotAllowed: "Method Not Allowed",
            StatusCode.InternalServerError: "Internal Server Error",
            StatusCode.NotImplemented: "Not Implemented",
        }[self]
