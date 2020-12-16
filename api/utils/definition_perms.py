from typing import Final


class PG_CATALOG:
    """
    This encapsulate the CATALOGS perms groups keys (PG means permission group)
    """
    LIST: Final[str] = "P_CATALOG_LIST"
    VIEW: Final[str] = "P_CATALOG_VIEW"
    CREATE: Final[str] = "P_CATALOG_CREATE"
    EDIT: Final[str] = "P_CATALOG_EDIT"
    DELETE: Final[str] = "P_CATALOG_DELETE"
