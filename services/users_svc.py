from typing import List, Union
from models.user import User, UserPwd
from .base_svc import BaseSvc
from api.utils.definition_types import DQueryData
from dal.db.user_db import UserDB
from api.utils.helpers import chunker
from config.config import CONFIGS


class UsersSvc(BaseSvc):
    """
    User services
    """
    db_repo: UserDB

    def __init__(self):
        self.db_repo = UserDB()

    async def get_all(self) -> List[User]:
        return await self.db_repo.get_all()

    async def get_count(self) -> int:
        return await self.db_repo.get_collection_count()

    async def get_parametrized(self, query_data: DQueryData) -> List[User]:
        return await self.db_repo.get_parametrized(query_data)

    async def get_by_id(self, user_id: str) -> Union[None, User, UserPwd]:
        object_id_dto = self.chk_object_id(user_id)
        result_db = await self.db_repo.get_by_id(object_id_dto)

        if result_db is None: self.RiseHTTP_NotFound()
        return result_db

    async def get_by_username (self, username: str) -> Union[None, User, UserPwd]:
        result_db = await self.db_repo.get_by_username(username)

        if result_db is None: self.RiseHTTP_NotFound()
        return result_db
