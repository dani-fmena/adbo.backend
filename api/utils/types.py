from typing import TypedDict


class DQueryData (TypedDict):
    skip: int
    limit: int
    field: str
    dir: str
