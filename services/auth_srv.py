from typing import Union, Optional
from api.utils.crypt import chk_pwd, mk_jwt_token
from .base_serv import BaseService
from models.user import UserPwd
from models.auth import AccessToken
from dal.db.user_db import UserDB
from api.utils.definition_types import AccessTokenMkMode


class AuthServices(BaseService):
    """
    Authentication service
    """
    db_repo: UserDB

    def __init__(self):
        self.db_repo = UserDB()

    async def authenticate_user(self, username: str, pwd: str) -> Union[None, UserPwd]:
        """
        Try to authenticate the user. If can't auth the user then return None. Notice that the returned user contains the secret hashed password
        :param username: The username to auth the user trough
        :param pwd: The plain string password
        :return: User if auth, None otherwise
        """
        user_db: Union[None, UserPwd] = await self.db_repo.get(username)

        if not user_db: self.RiseHTTP_NotFound()
        if not chk_pwd(pwd, user_db.pwd): self.RaiseHTTP_Unauthorized()
        return user_db

    async def mk_access_token(self, subject: str, subject_mode: Optional[AccessTokenMkMode] = None) -> AccessToken:
        """
        Service wrapper for Oauth2 compliant bearer access token creation.
        :param subject: The subject to authenticate
        :param subject_mode: Identifies the kind of owner for the generated access token. It's going to be used on the subject
        :return: The generated token
        """
        mode: str = AccessTokenMkMode.web_front.value if not subject_mode else subject_mode.value
        access_token = mk_jwt_token({'sub': mode + ':' + subject})

        return AccessToken(access_token = access_token, token_type = 'bearer')
