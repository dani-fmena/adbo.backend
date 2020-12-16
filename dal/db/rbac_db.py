from typing import Union
from models.rbac import Perm
from dal.db.base_db import BaseDB
from .collections import DBCollections


class RbacDB(BaseDB):
    """
    Database MongoDB access related to the user entity
    """

    def __init__(self):
        super().__init__(DBCollections.PERMS)

    async def get_perm(self, perm_name: str, user_rol_name: str) -> Union[None, Perm]:
        """
        Get the permission document from the database by the permission name and the rol name
        :param perm_name: name of the permission
        :param user_rol_name: name of the user rol for filtering purpose
        :return:
        """
        perm = await self.collection.find_one({'name': perm_name, 'roles.role': user_rol_name})
        return Perm(**perm) if perm else None
