from typing import List


class CONFIGS:
    MONGO_DETAILS = "mongodb://localhost:27017"
    CHUNK_SIZE = 1000                                           # the number chunk the input data to try to process it by chunks

    # use this to allow origin api request to the CORS middleware protection
    ORIGINS: List[str]  = [
        "http://localhost:8080",
    ]
