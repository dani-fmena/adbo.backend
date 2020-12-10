from pydantic import BaseModel
from typing import Optional


class AccessToken(BaseModel):
    access_token: str
    token_type: str


# maybe if the JWT token increase the amount of fields we can use this class of a TypeDic instead for describing the data
class TokenData(BaseModel):
    username: Optional[str] = None
