from typing import Final, Dict
from api.utils.definition_types import DException


class TAGS:
    AUTH: Final[str] = "Authorization & Authentication"
    CATALOG: Final[str] = "Catalog"
    USERS: Final[str] = "User"
    CATEGORY: Final[str] = "Category"
    DEV: Final[str] = "Development Only"


class SDES:  # http status code description
    # TODO when i18n is done in the front, return string key likes here, and translate then in the front
    NOTFOUND: Final[DException] = DException(msg = 'Entity not found')
    FORBIDDEN: Final[DException] = DException(msg = 'Forbidden')
    FORBIDDEN_RBAC: Final[DException] = DException(msg = 'The user isn\'t allowed to make this request')
    UNAUTHORIZED: Final[DException] = DException(msg = 'Could not validate credentials')
    CREATED: Final[DException] = DException(msg = 'Created')
    NO_CONTENT: Final[DException] = DException(msg = 'There is no content')
    BAD_REQUEST: Final[DException] = DException(msg = 'The request data was invalid')
    DAL_FAIL: Final[DException] = DException(msg = 'DAL fails the ops')
    DAL_FAIL_EMPTY: Final[DException] = DException(msg = 'DAL fails. No records modified')
    UNPROCESSABLE_ENTITY: Final[DException] = DException(msg = 'Something is wrong with the input')


class RESPHEADER:  # http response headers
    UNAUTHORIZED_BEARER: Final[Dict[str, str]] = {"WWW-Authenticate": "Bearer"}
    UNAUTHORIZED_RESOURCE: Final[Dict[str, str]] = {"WWW-Authenticate": "Resource"}


tags_metadata = [
    {"name": TAGS.AUTH, "description": "Auth endpoints ops"},
    {"name": TAGS.CATALOG, "description": "Catalogs operations"},
    {"name": TAGS.CATEGORY, "description": "Category operations"},
    {"name": TAGS.DEV, "description": "Ops just for development process"}
]
