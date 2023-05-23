from serverhttpy.exceptions.invalid_path_structure import InvalidPathStructureException
from serverhttpy.exceptions.invalid_query_param_structure import (
    InvalidQueryParamStructureException,
)
from serverhttpy.models.path import Path


class URI:
    path: Path
    query_params: dict

    def __str__(self):
        base = f"{self.path}"
        if len(self.query_params) > 0:
            base += "?"
            for index, param in enumerate(self.query_params):
                base += f"{param}={self.query_params[param]}"
                if index < len(self.query_params) - 1:
                    base += "&"
        return base

    def __init__(self, path_string: str):
        path_elems = path_string.split("?")

        if 1 > len(path_elems) > 2:
            raise InvalidPathStructureException(path_string)

        self.path = Path(path_elems[0])
        self.query_params = dict()

        if len(path_elems) > 1:
            query_params = path_elems[1].split("&")
            for param in query_params:
                key_value = param.split("=")

                if len(key_value) != 2:
                    raise InvalidQueryParamStructureException(param)

                self.query_params[key_value[0]] = key_value[1]
