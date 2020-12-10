from typing import Union
from models.user import UserPwd, User
from dal.db.base_db import BaseDB
from .collections import DBCollections


class UserDB(BaseDB):
    """
    Database MongoDB access related to the user entity
    """

    def __init__(self):
        super().__init__(DBCollections.USERS)

    async def get(self, username: str, with_private_data = False) -> Union[None, UserPwd, User]:
        """
        Get a specific user from database
        :param username: The username to auth the user trough
        :param with_private_data: If we should retrieve the user private data
        :return: The user to find or None if the username missing
        """
        db_user = await self.collection.find_one({"username": username})

        if db_user: return UserPwd(**db_user) if with_private_data else User(**db_user)
        else: return None
