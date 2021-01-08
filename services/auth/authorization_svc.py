from typing import Union
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from services.base_svc import BaseSvc
from api.utils.crypt import decode_jwt_token
from dal.db.user_db import UserDB
from dal.db.rbac_db import RbacDB
from models.user import UserPwd
from api.utils.definition_types import DTokenData, DException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")      # relative path to the get access token url. Set to use the PASSWORD Oauth2 flow


class AuthorizationSvc(BaseSvc):
    """
    Authorization service
    """
    db_user_repo: UserDB
    db_rbac_repo: RbacDB
    permission: str

    def __init__ (self, perm: str = None):
        """
        :param perm: The permission to be checked. Can be NONE
        """
        self.db_user_repo = UserDB()
        self.db_rbac_repo = RbacDB()
        self.permission = perm

    async def __call__ (self, token: str = Depends(oauth2_scheme)):
        # decoding the token ended in the request
        payload: DTokenData = decode_jwt_token(token = token)
        if not payload: self.RiseHTTP_Unauthorized()

        # getting and checking the user
        user: UserPwd = await self.chk_user(payload.get('sub'))

        # check user perm/role, RBAC authorization
        await self.chk_authorization(user)

        return user

    async def chk_user (self, username: str) -> UserPwd:
        """
        Check if the user exist and is an active user
        :return: The user
        """
        if not username: self.RiseHTTP_Unauthorized()

        # TODO !!! this query it's extremely frequent, a viable solution may need a redis for cache. The cache layer should not be here
        user_db: Union[None, UserPwd] = await self.db_user_repo.get_by_username(username)

        if not user_db: self.RiseHTTP_NotFound(DException(msg = 'The user owner of the auth access token is missing from our records'))  # the user isn't exist
        if not user_db.isEnable: self.RiseHTTP_BadRequest(DException(msg = 'Inactive user'))  # the user isn't enable

        return user_db

    async def chk_authorization (self, user: UserPwd) -> bool:
        """
        Check if the user has the permission to do the request operation / resource
        :param user: user request
        :return: True user has the perm
        """
        # TODO !!! this query it's extremely frequent, a viable solution may need a redis for cache. The cache layer should not be here
        db_perm = await self.db_rbac_repo.get_perm(self.permission, user.role)
        return True if db_perm else self.RiseHTTP_Forbidden()
