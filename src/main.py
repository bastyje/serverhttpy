from enums.status_code import StatusCode
from models.path import Path
from models.request import Request
from models.response import Response
from server import Server

# Example usage of Server

if __name__ == '__main__':
    def index(request: Request):
        return Response(StatusCode.OK, 'HTTP/1.1', body='data', headers={
            'Content-Type': 'text/plain'
        })

    server = Server('0.0.0.0', 8080)
    server.register_action(Path('/'), index)
    server.serve()
