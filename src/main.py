import time

from httpy.enums.http_method import HTTPMethod
from httpy.enums.status_code import StatusCode
from httpy.models.endpoint import Endpoint
from httpy.models.path import Path
from httpy.models.request import Request
from httpy.models.response import Response
from httpy.server import Server

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
