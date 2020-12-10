from typing import List


class CONFIGS:
    MONGO_DETAILS = 'mongodb://localhost:27017'
    CHUNK_SIZE = 1000                                           # the number chunk the input data to try to process it by chunks

    # use this to allow origin api request to the CORS middleware protection
    ORIGINS: List[str] = [
        'http://localhost:8080'
    ]

    # auth
    SECRET_KEY = '072b2926c45878764f9c0fc5ddd8ec633e6ecdc84147f91bbfd383de60b472a3'     # openssl rand -hex 32
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 1440                           # 24 hrs
