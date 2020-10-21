from typing import List


class CONFIGS:
    MONGO_DETAILS = "mongodb://localhost:27017"

    # use this to allow origin api request to the CORS middleware protection
    ORIGINS: List[str]  = [
        "http://localhost:8080",
    ]
