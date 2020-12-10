from models.entity import EntityM, DateEntity
from typing import Optional


class User(EntityM, DateEntity):
    username: str
    email: Optional[str] = None
    fullName: Optional[str] = None
    isEnable: Optional[bool] = None


class UserPwd(User):
    pwd: str
