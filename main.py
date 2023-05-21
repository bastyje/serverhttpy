import time

from pyhttp.enums.http_method import HTTPMethod
from pyhttp.enums.status_code import StatusCode
from pyhttp.models.endpoint import Endpoint
from pyhttp.models.path import Path
from pyhttp.models.request import Request
from pyhttp.models.response import Response
from pyhttp.server import Server

# Example usage of Server

if __name__ == '__main__':
    def index(request: Request) -> Response:
        time.sleep(1.0)
        return Response(StatusCode.OK, body='data', headers={
            'Content-Type': 'text/plain'
        })
    
    # def say_name_and_age(request: Request) -> Response:
    #     print(request.request_arguments)
    #     name = request.request_arguments['name']
    #     age = request.request_arguments['age']
    #     body = 'Your name is {name} and you are {age} years old!'.format(name = name, age = age)
    #     print(body)
    #     return Response(StatusCode.OK, body=body, headers={
    #         'Content-Type': 'text/plain'
    #     })

    server = Server('0.0.0.0', 8080, threads_number=10)
    server.register_endpoint(Endpoint(Path('/movie'), HTTPMethod.POST, index))
    # server.register_endpoint(Endpoint(Path('/{name}/{age}'), HTTPMethod.GET, say_name_and_age))
    server.serve()
