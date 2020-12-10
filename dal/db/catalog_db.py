from typing import List
from bson import ObjectId
from datetime import datetime
from typing import Union
from pymongo.results import UpdateResult, InsertOneResult, DeleteResult
from dal.db.base_db import BaseDB, SanitationMode
from models.catalog import Catalog
from api.utils.definition_types import DQueryData
from .collections import DBCollections


class CatalogDB(BaseDB):
    """
    Database MongoDB access related to the catalog entity
    """

    def __init__(self):
        super().__init__(DBCollections.CATALOGS)

    async def get_all(self) -> List[Catalog]:
        """
        Retrieve all catalog from the database

        :return: List of catalogs
        """
        catalogs: List = []

        async for catalog in self.collection.find():
            catalogs.append(Catalog(**catalog))

        return catalogs

    async def get_collection_count(self) -> int:
        return await self.collection.estimated_document_count()

    async def get_parametrized(self, q: DQueryData) -> List[Catalog]:      # qd means query data
        """
        Gets the catalogs in a parametrized way with the query params
        """
        # This kind of pagination have a very poor performance, but allows random navigation through pages.
        catalogs: List = []

        if q['dir'] is None or q['field'] is None:     # with sorting by field
            catalogs_db = self.collection.find().skip(q['skip']).limit(q['limit']) if q['search'] is None \
                else self.collection.find({'name': {'$regex': '.*' + q['search'] + '.*'}}).limit(q['limit'])
        else:                                           # without sorting
            catalogs_db = self.collection.find().skip(q['skip']).limit(q['limit']).sort(q['field'], q['dir']) if q['search'] is None \
                else self.collection.find({'name': {'$regex': '.*' + q['search'] + '.*'}}).limit(q['limit']).sort(q['field'], q['dir'])

        async for catalog in catalogs_db: catalogs.append(Catalog(**catalog))
        return catalogs

    async def get(self, catalog_object_id: ObjectId) -> Union[None, Catalog]:
        """
        Get a specific catalog and try to find it

        :return: The catalog to find or None if the id is missing
        """

        db_catalog = await self.collection.find_one({"_id": catalog_object_id})

        if db_catalog: return Catalog(**db_catalog)
        else: return None

    async def create(self, catalog_dto: Catalog) -> Union[bool, InsertOneResult]:
        """
        Created a new catalog in to the database

        :param catalog_dto: The Catalog to be added
        :return: The new added already catalog object
        """

        catalog_dto.createdAt = datetime.utcnow()

        self.id_sanitation(catalog_dto)                                                          # if the dto has id, we remove it
        self.date_sanitation(SanitationMode.rm_update_date, catalog_dto)                         # Update date sanitation

        try: q_result: InsertOneResult = await self.collection.insert_one(catalog_dto.dict(by_alias = True))
        except: return False

        return q_result

    async def update(self, catalog_dto: Catalog) -> Union[bool, UpdateResult]:

        self.date_sanitation(SanitationMode.rm_create_date, catalog_dto)                         # Update date sanitation
        catalog_dto.updatedAt = datetime.utcnow()

        try: q_result: UpdateResult = await self.collection.update_one(
            {'_id': catalog_dto.id},
            {'$set': catalog_dto.dict(by_alias = True, exclude_none = True)})
        except: return False

        return q_result

    async def delete(self, catalog_object_id: ObjectId) -> Union[None, bool, Catalog]:
        catalog_db = await self.collection.find_one({'_id': catalog_object_id})

        if catalog_db:
            try: await self.collection.delete_one({'_id': catalog_object_id})
            except: return False                         # something was wrong
        else: return None                                # 404

        return Catalog(**catalog_db)

    async def set_status(self, catalog_object_id: ObjectId, new_status: bool) -> Union[bool, UpdateResult]:
        """
        Set a new status for the Catalog, according to the new_status parameter.

        :rtype: Catalog
        """

        try:
            q_result: UpdateResult = await self.collection.update_one(
                {'_id': catalog_object_id},
                {'$set': {
                    'isEnable':  new_status,
                    'updatedAt': datetime.utcnow()
                }}
            )
        except: return False

        return q_result

    async def bulk_set_status(self, ids: List[ObjectId], new_status: bool) -> Union[bool, UpdateResult]:
        """
        Enable or Disable the IDs object in bulk (update_many) according to the new_status parameter

        :param new_status: The new status of the objects/documents
        :param ids: The objects/documents to be changed
        :return:
        """
        q_result: UpdateResult

        updated_at = datetime.utcnow()

        try:
            q_result = await self.collection.update_many(
                {"_id": {"$in": ids}},
                {"$set": {
                    "isEnable":  new_status,
                    "updatedAt": updated_at
                }}
            )
        except: return False

        return q_result

    async def bulk_remove(self, ids: List[ObjectId]) -> Union[None, bool]:
        """
        Remove the IDs object in bulk

        :param ids: The objects/documents to be removed
        :return:
        """
        q_result: DeleteResult

        try: q_result: DeleteResult = await self.collection.delete_many({"_id": {"$in": ids}})
        except: return False

        return True if q_result.deleted_count > 0 else None
