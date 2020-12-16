from typing import TypedDict, Union


class DException(TypedDict):
    msg: str


class DQueryData(TypedDict):
    skip: int
    limit: int
    field: Union[str, None]
    dir: Union[str, None]
    search: Union[str, None]


class DTokenData(TypedDict):
    sub: str                                                        # subject -> username
