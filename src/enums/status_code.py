from enum import Enum


class StatusCode(Enum):
    OK = 200
    BadRequest = 400
    NotFound = 404
    InternalServerError = 500

    def description(self):
        return {
            StatusCode.OK: 'OK',
            StatusCode.BadRequest: 'Bad Request',
            StatusCode.NotFound: 'Not Found',
            StatusCode.InternalServerError: 'Internal Server Error'
        }[self]
