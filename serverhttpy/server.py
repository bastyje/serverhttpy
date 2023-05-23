import multiprocessing as mp
import socket
import traceback
from typing import Dict

from serverhttpy.enums.status_code import StatusCode
from serverhttpy.exceptions.invalid_request_structure import (
    InvalidRequestStructureException,
)
from serverhttpy.exceptions.unsupported_method_specified import (
    UnsupportedMethodSpecifiedException,
)
from serverhttpy.models.endpoint import Endpoint
from serverhttpy.models.request import Request
from serverhttpy.models.response import Response


class Server:
    __ip: str
    __port: int
    __endpoints: Dict[Endpoint, Endpoint]
    __bufsize: int
    __threads_number: int

    def __init__(
        self,
        ip: str,
        port: int = 80,
        protocol: str = "HTTP/1.1",
        bufsize: int = 8192,
        threads_number: int = mp.cpu_count(),
    ):
        self.__ip = ip
        self.__port = port
        self.__endpoints = dict()
        self.__protocol = protocol
        self.__bufsize = bufsize
        self.__threads_number = threads_number

    def serve(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.__ip, self.__port))
        server_socket.listen(20)

        print(f"Listening on {self.__ip}:{self.__port}")

        processes = list()
        lock = mp.Lock()

        try:
            for i in range(self.__threads_number):
                processes.append(
                    mp.Process(target=self.__serve_loop, args=(server_socket, lock))
                )
                processes[i].start()
        finally:
            server_socket.close()
            for i in range(self.__threads_number):
                try:
                    processes[i].join()
                    processes[i].terminate()
                except KeyboardInterrupt:
                    pass
            print("Server stopped")

    def __serve_loop(self, server_socket: socket.socket, lock: mp.Lock):
        try:
            while True:
                lock.acquire()
                client_connection, client_address = server_socket.accept()
                request = client_connection.recv(self.__bufsize)
                lock.release()

                response = self.__handle_request(request.decode())

                client_connection.sendall(response.encode())
                client_connection.close()
        except KeyboardInterrupt:
            pass

    def register_endpoint(self, endpoint: Endpoint):
        self.__endpoints[endpoint] = endpoint

    def __execute_action(self, request: Request) -> Response:
        potential_endpoints = []
        searched_endpoint = None
        for endpoint in self.__endpoints:
            if Server.__compare_paths(
                endpoint.path.path_elements, request.uri.path.path_elements
            ):
                potential_endpoints.append(endpoint)
        if len(potential_endpoints) == 0:
            return Response(StatusCode.NotFound)
        elif len(potential_endpoints) > 1:
            searched_endpoint = Server.__get_correct_endpoint(
                potential_endpoints, request.uri.path.path_elements
            )
        else:
            searched_endpoint = potential_endpoints[0]
        request.request_arguments = Server.__retrieve_arguments(
            searched_endpoint.path.path_elements, request.uri.path.path_elements
        )
        return searched_endpoint.execute(request)

    def __handle_request(self, request_string: str) -> str:
        request: Request | None = None
        response: Response | None = None

        try:
            request = Request(request_string)
            print(f"Handling request|{request}")
            response = self.__execute_action(request)
        except UnsupportedMethodSpecifiedException as e:
            response = Response(StatusCode.NotImplemented, body=str(e))
        except InvalidRequestStructureException as e:
            response = Response(StatusCode.BadRequest, body=str(e))
        except Exception as e:
            traceback.print_exc()
            response = Response(StatusCode.InternalServerError, body=str(e))
        finally:
            print(f"Request finished|{request}|{response}")
            return repr(response)

    def __compare_paths(endpoint_path_elements, request_path_elements):
        endpoint_elements_keys = list(endpoint_path_elements.keys())
        request_elements_keys = list(request_path_elements.keys())
        if len(endpoint_elements_keys) != len(request_elements_keys):
            return False
        for i in range(len(endpoint_path_elements)):
            endpoint_key = endpoint_elements_keys[i]
            if endpoint_path_elements[endpoint_key] == True:
                endpoint_elements_keys[i] = "/"
                request_elements_keys[i] = "/"
            else:
                endpoint_elements_keys[i] += "/"
                request_elements_keys[i] += "/"
        return endpoint_elements_keys == request_elements_keys

    def __get_correct_endpoint(potential_endpoints, request_path_elements):
        path_elements_keys = list(request_path_elements.keys())
        for i in range(len(path_elements_keys)):
            all_none = True
            for endpoint in potential_endpoints:
                endpoint_path_keys = list(endpoint.path.path_elements.keys())

                if path_elements_keys[i] in endpoint_path_keys:
                    all_none = False
            if not all_none:
                for endpoint in potential_endpoints:
                    if (
                        not path_elements_keys[i]
                        == list(endpoint.path.path_elements.keys())[i]
                    ):
                        potential_endpoints.remove(endpoint)
        return potential_endpoints[0]

    def __retrieve_arguments(endpoint_path_elements, request_path_elements):
        arguments = dict()
        endpoint_elements_keys = list(endpoint_path_elements.keys())
        request_elements_keys = list(request_path_elements.keys())
        for i in range(len(endpoint_path_elements)):
            endpoint_key = endpoint_elements_keys[i]
            if endpoint_path_elements[endpoint_key] == True:
                arguments[endpoint_key] = request_elements_keys[i]

        return arguments
