from typing import Union
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from api.utils.crypt import chk_pwd, mk_jwt_token, decode_jwt_token
from .base_serv import BaseService
from models.user import UserPwd, User
from models.auth import AccessToken
from dal.db.user_db import UserDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")      # relative path to the get access token url. Set to use the PASSWORD Oauth2 flow


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
        user_db: Union[None, UserPwd] = await self.db_repo.get(username, True)

        if not user_db: self.RiseHTTP_NotFound()
        if not chk_pwd(pwd, user_db.pwd): self.RaiseHTTP_Unauthorized(is_gen_auth_tk = True)
        return user_db

    @staticmethod
    async def mk_access_token(subject: str) -> AccessToken:
        """
        Service wrapper for Oauth2 compliant bearer access token creation.
        :param subject: The subject to authenticate
        :return: The generated token
        """
        return AccessToken(access_token = mk_jwt_token({'sub': subject}), token_type = 'bearer')

    @staticmethod
    async def request_user(token: str = Depends(oauth2_scheme)) -> User:
        payload: dict = decode_jwt_token(token = token)
        if not payload: BaseService.RaiseHTTP_Unauthorized()

        username = payload.get('sub')
        if not username: BaseService.RaiseHTTP_Unauthorized()

        # TODO this query it's extremely frequent, a pro solution may need a redis for cache
        db_repo = UserDB()
        user_db: Union[None, UserPwd] = await db_repo.get(username)
        if not user_db: BaseService.RiseHTTP_NotFound(details = "The user owner of the auth access token is missing from our records")
        if not user_db.isEnable: BaseService.RiseHTTP_BadRequest(details = "Inactive user")

        return user_db
