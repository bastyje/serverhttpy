import time

from serverhttpy.enums.http_method import HTTPMethod
from serverhttpy.enums.status_code import StatusCode
from serverhttpy.models.endpoint import Endpoint
from serverhttpy.models.path import Path
from serverhttpy.models.request import Request
from serverhttpy.models.response import Response
from serverhttpy.server import Server

from sample_data import Sample_data

# Example usage of Server

data = Sample_data()

if __name__ == "__main__":

    def index(request: Request) -> Response:
        time.sleep(1.0)
        return Response(
            StatusCode.OK, body="Welcome!", headers={"Content-Type": "text/plain"}
        )

    def say_name_and_age(request: Request) -> Response:
        name = request.request_arguments["name"]
        age = request.request_arguments["age"]
        body = "Your name is {name} and you are {age} years old!".format(
            name=name, age=age
        )
        return Response(
            StatusCode.OK, body=body, headers={"Content-Type": "text/plain"}
        )

    def get_clients(request: Request) -> Response:
        body = "Clients:\n"
        clients_keys = data.clients.keys()
        for key in clients_keys:
            body += "{key} - {client}\n".format(key=key, client=data.clients[key])
        return Response(
            StatusCode.OK, body=body, headers={"Content-Type": "text/plain"}
        )

    # idk why it isn`t working xd
    def add_client(request: Request) -> Response:
        clientId = request.request_arguments["clientId"]
        clientName = request.request_arguments["clientName"]
        clientSurname = request.request_arguments["clientSurname"]
        body = ""
        if clientId in list(data.clients.keys()):
            body = "Client with id {clientId} already exists!".format(clientId=clientId)
            return Response(
                StatusCode.BadRequest, body=body, headers={"Content-Type": "text/plain"}
            )
        data.update_clients(
            clientId,
            "{clientName} {clientSurname}".format(
                clientName=clientName, clientSurname=clientSurname
            ),
        )
        body = "Client with Id {clientId} Name and surname {clientName} {clientSurname} added".format(
            clientId=clientId, clientName=clientName, clientSurname=clientSurname
        )
        return Response(
            StatusCode.OK, body=body, headers={"Content-Type": "text/plain"}
        )

    def get_client(request: Request) -> Response:
        body = ""
        clientId = request.request_arguments["clientId"]
        if not clientId in data.clients.keys():
            body = "Client with Id {clientId} not found".format(clientId=clientId)
        else:
            body = "Client with Id {clientId}:\n{client}".format(
                clientId=clientId, client=data.clients[clientId]
            )
        return Response(
            StatusCode.OK, body=body, headers={"Content-Type": "text/plain"}
        )

    def client_case_information(request: Request) -> Response:
        clientId = request.request_arguments["clientId"]
        caseId = request.request_arguments["caseId"]

        body = ""
        if not clientId in data.clients.keys():
            body = "Client with Id {clientId} not found"
        clientCaseId = data.clients_cases[clientId]
        clientCase = data.cases[clientCaseId]
        body = (
            "Client with id {clientId}: {client}\nCase on client: {clientCase}".format(
                clientId=clientId, client=data.clients[clientId], clientCase=clientCase
            )
        )
        return Response(
            StatusCode.OK, body=body, headers={"Content-Type": "text/plain"}
        )

    server = Server("0.0.0.0", 8080, threads_number=10)
    server.register_endpoint(Endpoint(Path("/"), HTTPMethod.GET, index))
    server.register_endpoint(
        Endpoint(Path("/{name}/{age}"), HTTPMethod.GET, say_name_and_age)
    )
    server.register_endpoint(Endpoint(Path("/clients"), HTTPMethod.GET, get_clients))
    server.register_endpoint(
        Endpoint(
            Path("/clients/{clientId}/{clientName}/{clientSurname}"),
            HTTPMethod.POST,
            add_client,
        )
    )
    server.register_endpoint(
        Endpoint(Path("/clients/{clientId}"), HTTPMethod.GET, get_client)
    )
    server.register_endpoint(
        Endpoint(
            Path("/clients/{clientId}/cases/{caseId}"),
            HTTPMethod.GET,
            client_case_information,
        )
    )
    server.serve()
