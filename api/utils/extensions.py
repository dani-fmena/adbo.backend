import pymongo
from api.utils.definition_types import DQueryData


async def dt_query_params(skip: int = 0, limit: int = 10, field: str = '', sortdir: str = '', search: str = '') -> DQueryData:
    """
    Common extension method for parametrized data (pagination, sorting and search) in to the query endpoint. DataTable Query Parameters

    :param skip: Records for skip
    :param limit: Records to select/retrieve
    :param field: Field of the entity to sort by
    :param sortdir: Directions for the sort: ascending, descending or none
    :param search: The search criteria

    :return: Return a dict with the query data
    """
    q: DQueryData = DQueryData(skip = skip, limit = limit, field = None, dir = None, search = None)

    if sortdir != '' and field != '':
        q['field'] = field
        q['dir'] = pymongo.ASCENDING if sortdir == 'asc' else pymongo.DESCENDING
    if search != '':
        q['search'] = search

    return q
