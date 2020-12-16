from typing import Optional, Union
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError
from config.config import CONFIGS
from api.utils.definition_types import DTokenData

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def chk_pwd(plain: str, hashed) -> bool:
    """
    Check if a secret plain password match with previously saved password (bcrypt)

    :arg plain: The secret plain password known by someone
    :arg hashed: The previously saved hashed password
    :return: True (match) False (doesn't match)
    """
    return pwd_context.verify(plain, hashed)


def hash_pwd(plain: str):
    """
    Give the hash using bcrypt algorithm

    :arg plain: The secret plain password known by someone
    :return: Hash
    """
    return pwd_context.hash(plain)


def mk_jwt_token(claims: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT token with an specific expiration time (default 24 hrs)
    :param claims: The claims data to be encoded in the JWT token
    :param expires_delta: Time delta to be use to specify the expiration time
    :return: The JTW sign & encoded token string
    """
    to_encode = claims.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes = CONFIGS.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, CONFIGS.SECRET_KEY, algorithm = CONFIGS.ALGORITHM)


def decode_jwt_token(token: str) -> Union[None, DTokenData]:
    """
    Try to decode a JWT token in to a dictionary
    :param token: A signed JWT to be verified
    :return: A dictionary with the payload data decoded
    """
    try:
        payload = jwt.decode(token, CONFIGS.SECRET_KEY, algorithms = CONFIGS.ALGORITHM)
    except JWTError: return None
    return payload

