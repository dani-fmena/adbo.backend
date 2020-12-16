from pydantic import BaseModel
from typing import Optional


class AccessToken(BaseModel):
    access_token: str
    token_type: str
