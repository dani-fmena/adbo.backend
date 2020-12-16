from typing import Union
from api.utils.crypt import chk_pwd, mk_jwt_token
from services.base_svc import BaseSvc
from models.user import UserPwd
from models.auth import AccessToken
from dal.db.user_db import UserDB


class AuthenticationSvc(BaseSvc):
    """
    Authentication service
    """
    db_repo: UserDB

    def __init__(self):
        self.db_repo = UserDB()

    def __call__(self, perm = ''):
        print('this is the perm ->' + perm)

    async def authenticate_user(self, username: str, pwd: str) -> Union[None, UserPwd]:
        """
        Try to authenticate the user. If can't auth the user then return None. Notice that the returned user contains the secret hashed password
        :param username: The username to auth the user trough
        :param pwd: The plain string password
        :return: User if auth, None otherwise
        """
        user_db: Union[None, UserPwd] = await self.db_repo.get(username, True)

        if not user_db: self.RiseHTTP_NotFound()
        if not chk_pwd(pwd, user_db.pwd): self.RiseHTTP_Unauthorized(is_gen_auth_tk = True)
        return user_db

    @staticmethod
    async def create_token(subject: str) -> AccessToken:
        """
        Service wrapper for Oauth2 compliant bearer access token creation.
        :param subject: The subject to authenticate
        :return: The generated token
        """
        return AccessToken(access_token = mk_jwt_token({'sub': subject}), token_type = 'bearer')


