from typing import Final, Dict


class CONFIGS:
    MONGO_DETAILS = "mongodb://localhost:27017"         # TODO move this to a config or env file


class TAGS:
    CATALOG: Final[str] = "Catalog"
    CATEGORY: Final[str] = "Category"


class SDES:  # http status code description
    NOTFOUND: Dict[str, str] = {"description": "Not found"}
    FORBIDDEN: Dict[str, str] = {"description": "Forbidden"}
    CREATED: Dict[str, str] = {"description": "Created"}


class SCODE:  # http status code number
    c404: int = 404
    c403: int = 403
    c201: int = 201
