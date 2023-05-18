import time

from serverhttpy.enums.http_method import HTTPMethod
from serverhttpy.enums.status_code import StatusCode
from serverhttpy.models.endpoint import Endpoint
from serverhttpy.models.path import Path
from serverhttpy.models.request import Request
from serverhttpy.models.response import Response
from serverhttpy.server import Server

# Example usage of Server

if __name__ == '__main__':
    def index(request: Request) -> Response:
        time.sleep(1.0)
        return Response(StatusCode.OK, body='data', headers={
            'Content-Type': 'text/plain'
        })

    server = Server('0.0.0.0', 8080, threads_number=10)
    server.register_endpoint(Endpoint(Path('/movie'), HTTPMethod.POST, index))
    server.serve()
