from typing import Final, Dict


class TAGS:
    CATALOG: Final[str] = "Catalog"
    CATEGORY: Final[str] = "Category"


class SDES:  # http status code description
    NOTFOUND: Dict[str, str] = {"description": "Entity not found"}
    FORBIDDEN: Dict[str, str] = {"description": "Forbidden"}
    CREATED: Dict[str, str] = {"description": "Created"}
    NOCONTENT: Dict[str, str] = {"description": "There is no content"}
    BADREQUEST: Dict[str, str] = {"description": "The request is invalid"}


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
