class Sample_data:
    clients: dict
    cases: dict
    clients_cases: dict

    def __init__(self):
        self.clients = {
            "1": "Marek Markowski",
            "2": "Czarek Czarkowski",
            "3": "Adam Adamowski",
        }
        self.cases = {
            "1": "Passport - New",
            "2": "Bank letter - In progress",
            "3": "Bank letter - Rejected",
        }
        self.clients_cases = {"1": "2", "2": "3", "3": "1"}

    def update_clients(self, key, value):
        self.clients[key] = value

    def update_cases(self, key, value):
        self.cases[key] = value

    def update_clients_cases(self, key, value):
        self.clients_cases[key] = value
