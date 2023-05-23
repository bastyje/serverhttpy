class Path:
    path: str
    # true means that element is an argument
    path_elements: dict

    def __init__(self, path: str):
        self.path = path
        self.path_elements = self.parse(path)

    def __str__(self):
        return self.path

    def __eq__(self, other):
        return isinstance(other, Path) and other.path == self.path

    def __hash__(self):
        return hash(self.path)

    def parse(self, path: str):
        elements = (path).split("/")
        elems = dict()
        for elem in elements:
            is_argument = Path.check_if_argument(elem)
            if is_argument:
                elem = elem[1:-1]
            elems[elem] = is_argument
        return elems

    def check_if_argument(element: str):
        return "{" in element and "}" in element
