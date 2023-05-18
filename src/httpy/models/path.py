class Path:
    path: str

    def __str__(self):
        return self.path

    def __eq__(self, other):
        return isinstance(other, Path) and other.path == self.path

    def __hash__(self):
        return hash(self.path)

    def __init__(self, path: str):
        self.path = path
