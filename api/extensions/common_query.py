import pymongo
from api.utils.types import DQueryData


async def dt_query_params(skip: int = 0, limit: int = 10, field: str = '', sortdir: str = 'none') -> DQueryData:
    """
    Common extension method for setting pagination information in to the query endpoint. DataTable Query Parameters

    :param skip: Records for skip
    :param limit: Records to select/retrieve
    :param field: Field of the entity to sort by
    :param sortdir: Directions for the sort: ascending, descending or none

    :return: Return a dict with the query data
    """
    if sortdir == 'none': return DQueryData(skip = skip, limit = limit, field = field, dir = sortdir)
    else:
        processed_dir = pymongo.ASCENDING if sortdir == 'asc' else pymongo.DESCENDING
        return DQueryData(skip = skip, limit = limit, field = field, dir = processed_dir)
