from typing import Union
from models.user import UserPwd
from dal.db.base_db import BaseDB
from .collections import DBCollections


class UserDB(BaseDB):
    """
    Database MongoDB access related to the user entity
    """

    def __init__(self):
        super().__init__(DBCollections.USERS)

    async def get(self, username: str) -> Union[None, UserPwd]:
        """
        Get a specific catalog and try to find it
        :param username: The username to auth the user trough
        :return: The user to find or None if the username missing
        """
        db_user = await self.collection.find_one({"username": username})

        if db_user: return UserPwd(**db_user)
        else: return None
