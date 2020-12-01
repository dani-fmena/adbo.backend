from typing import Final, Dict


class TAGS:
    CATALOG: Final[str] = "Catalog"
    CATEGORY: Final[str] = "Category"
    DEV: Final[str] = "Development Only"


class SDES:  # http status code description
    # TODO when i18n is done in the front, return string key likes here, and translate then in the front
    NOTFOUND: Dict[str, str] = {"description": "Entity not found"}
    FORBIDDEN: Dict[str, str] = {"description": "Forbidden"}
    CREATED: Dict[str, str] = {"description": "Created"}
    NO_CONTENT: Dict[str, str] = {"description": "There is no content"}
    BAD_REQUEST: Dict[str, str] = {"description": "The request data was invalid"}
    DAL_FAIL: Dict[str, str] = {"description": "DAL fails the ops"}
    DAL_FAIL_EMPTY: Dict[str, str] = {"description": "DAL fails. No records modified"}
    UNPROCESSABLE_ENTITY: Dict[str, str] = {"description": "Something is wrong with the input"}


tags_metadata = [
    {
        "name": TAGS.CATALOG,
        "description": "Catalogs operations",
    },
    {
        "name": TAGS.CATEGORY,
        "description": "Category operations",
    }
]
