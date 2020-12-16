from typing import List
from pydantic import BaseModel
from models.entity import EntityM, DateEntity


class RoleId(BaseModel):
    role: str


class Role(EntityM, DateEntity):
    """
    User roles permission entity
    """
    name: str


class Perm(EntityM):
    """
    Permission entity
    """
    name: str
    group: str
    roles: List[RoleId]
