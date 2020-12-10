from enum import Enum
from typing import TypedDict, Union


class DQueryData (TypedDict):
    skip: int
    limit: int
    field: Union[str, None]
    dir: Union[str, None]
    search: Union[str, None]


class AccessTokenMkMode (Enum):
    web_front = 'web'
    app_front = 'app'
    service = 'srv'
