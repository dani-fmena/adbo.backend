from .collections import DBCollections
from typing import Union, List
from bson import ObjectId
from models.user import UserPwd, User
from dal.db.base_db import BaseDB
from api.utils.definition_types import DQueryData


class UserDB(BaseDB):
    """
    Database MongoDB access related to the user entity
    """

    def __init__(self):
        super().__init__(DBCollections.USERS)

    async def get_by_username(self, username: str, with_private_data = False) -> Union[None, UserPwd, User]:
        """
        Get a specific user from database
        :param username: The username to auth the user trough
        :param with_private_data: If we should retrieve the user private data
        :return: The user to find or None if the username missing
        """
        db_user = await self.collection.find_one({'username': username})

        if db_user: return UserPwd(**db_user) if with_private_data else User(**db_user)
        else: return None

    async def get_by_id(self, catalog_object_id: ObjectId, with_private_data = False) -> Union[None, UserPwd, User]:
        """
        Get a specific catalog from database

        :return: The catalog to find or None if the id is missing
        """
        db_user = await self.collection.find_one({"_id": catalog_object_id})

        if db_user: return UserPwd(**db_user) if with_private_data else User(**db_user)
        else: return None

    async def get_all(self) -> List[User]:
        """
        Retrieve all users from the database
        :return: List of catalogs
        """
        users: List = []

        async for catalog in self.collection.find():
            users.append(User(**catalog))

        return users

    async def get_collection_count(self) -> int:
        return await self.collection.estimated_document_count()

    async def get_parametrized(self, q: DQueryData) -> List[User]:      # qd means query data
        """
        Gets the users in a parametrized way with the query params
        """
        # This kind of pagination have a very poor performance, but allows random navigation through pages.
        users: List = []

        if q['dir'] is None or q['field'] is None:     # with sorting by field
            users_db = self.collection.find().skip(q['skip']).limit(q['limit']) if q['search'] is None \
                else self.collection.find({'name': {'$regex': '.*' + q['search'] + '.*'}}).limit(q['limit'])
        else:                                           # without sorting
            users_db = self.collection.find().skip(q['skip']).limit(q['limit']).sort(q['field'], q['dir']) if q['search'] is None \
                else self.collection.find({'name': {'$regex': '.*' + q['search'] + '.*'}}).limit(q['limit']).sort(q['field'], q['dir'])

        async for user in users_db: users.append(User(**user))
        return users
