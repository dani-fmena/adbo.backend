from typing import Dict


async def pagination_q(skip: int = 0, limit: int = 10) -> Dict:
    """
    Common extension method for setting pagination information in to the query endpoint

    :param skip: Records for skip
    :param limit: Records to select/retrieve
    :return: Return a dict with the queries
    """
    return {"skip": skip, "limit": limit}
