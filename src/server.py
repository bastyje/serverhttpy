import multiprocessing as mp
import socket
import traceback
from typing import Callable

from enums.status_code import StatusCode
from exceptions.invalid_request_structure import InvalidRequestStructureException
from models.path import Path
from models.request import Request
from models.response import Response


class Server:
    __ip: str
    __port: int
    __actions: dict
    __bufsize: int
    __threads_number: int

    def __init__(self, ip: str, port: int = 80, protocol: str = 'HTTP/1.1', bufsize: int = 8192, threads_number: int = mp.cpu_count()):
        self.__ip = ip
        self.__port = port
        self.__actions = dict()
        self.__protocol = protocol
        self.__bufsize = bufsize
        self.__threads_number = threads_number

    def serve(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.__ip, self.__port))
        server_socket.listen(20)

        print(f'Listening on {self.__ip}:{self.__port}')

        processes = list()
        recv_lock = mp.Lock()
        lock = mp.Lock()

        try:
            for i in range(self.__threads_number):
                processes.append(mp.Process(target=self.__serve_loop, args=(server_socket, lock)))
                processes[i].start()
        except KeyboardInterrupt:
            print('Server stopped')
        finally:
            server_socket.close()
            for i in range(self.__threads_number):
                processes[i].join()

    def __serve_loop(self, server_socket: socket.socket, lock: mp.Lock):
        while True:
            lock.acquire()
            client_connection, client_address = server_socket.accept()
            request = client_connection.recv(self.__bufsize)
            lock.release()

            response = self.__handle_request(request.decode())

            # lock.acquire()
            client_connection.sendall(response.encode())
            client_connection.close()
            # lock.release()

    def register_action(self, path: Path, action: Callable[[Request], Response]):
        self.__actions[path] = action

    def __execute_action(self, request: Request) -> Response:
        if request.uri.path not in self.__actions:
            return Response(StatusCode.NotFound, self.__protocol)
        else:
            return self.__actions[request.uri.path](request)

    def __handle_request(self, request_string: str) -> str:
        response: Response | None = None

        try:
            request = Request(request_string)
            print(f'Handling request|{request}')
            response = self.__execute_action(request)
        except InvalidRequestStructureException as e:
            response = Response(StatusCode.BadRequest, self.__protocol, body=str(e))
        except Exception as e:
            traceback.print_exc()
            response = Response(StatusCode.InternalServerError, self.__protocol, body=str(e))
        finally:
            print(f'Request finished with response|{response}')
            return repr(response)
