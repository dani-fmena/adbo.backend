from typing import Final, Dict


class TAGS:
    AUTH: Final[str] = "Authorization & Authentication"
    CATALOG: Final[str] = "Catalog"
    CATEGORY: Final[str] = "Category"
    DEV: Final[str] = "Development Only"


class SDES:  # http status code description
    # TODO when i18n is done in the front, return string key likes here, and translate then in the front
    NOTFOUND: Final[Dict[str, str]] = {"description": "Entity not found"}
    FORBIDDEN: Final[Dict[str, str]] = {"description": "Forbidden"}
    UNAUTHORIZED: Final[Dict[str, str]] = {"description": "Could not validate credentials"}
    CREATED: Final[Dict[str, str]] = {"description": "Created"}
    NO_CONTENT: Final[Dict[str, str]] = {"description": "There is no content"}
    BAD_REQUEST: Final[Dict[str, str]] = {"description": "The request data was invalid"}
    DAL_FAIL: Final[Dict[str, str]] = {"description": "DAL fails the ops"}
    DAL_FAIL_EMPTY: Final[Dict[str, str]] = {"description": "DAL fails. No records modified"}
    UNPROCESSABLE_ENTITY: Final[Dict[str, str]] = {"description": "Something is wrong with the input"}


class RESPHEADER:  # http response headers
    UNAUTHORIZED_BEARER: Final[Dict[str, str]] = {"WWW-Authenticate": "Bearer"}
    UNAUTHORIZED_RESOURCE: Final[Dict[str, str]] = {"WWW-Authenticate": "Resource"}


tags_metadata = [
    {"name": TAGS.AUTH, "description": "Auth endpoints ops"},
    {"name": TAGS.CATALOG, "description": "Catalogs operations"},
    {"name": TAGS.CATEGORY, "description": "Category operations"},
    {"name": TAGS.DEV, "description": "Ops just for development process"}
]
