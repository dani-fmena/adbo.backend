from pymongo.results import UpdateResult, InsertOneResult, DeleteResult
from pymongo.collection import Collection
from datetime import datetime
from typing import Union
from bson import ObjectId
from enum import Enum
from api.database import db
from models.catalog import Catalog
from typing import List
from models.entity import EntityM, Entity, DateEntity


class SanitationMode (Enum):
    rm_create_date = 1
    rm_update_date = 2
    rm_both_date = 3


class CatalogDB:
    """
    Database access related to the catalog entity
    """
    catalogs_db: Collection

    def __init__(self):
        self.catalogs_db = db.get_collection('catalogs')

    @staticmethod
    def __date_sanitation(mode: Enum, dto: Union[DateEntity]):
        """
        Depending of the parameter, we reset the corresponding date field in the DTO, so the DTO dont
        inject 'noise' and 'dirt' to the database.

        :rtype: None
        """
        if mode == SanitationMode.rm_both_date:     # reset the -createdAt- and -createdAt- field
            dto.createdAt = None
            dto.updatedAt = None
        if mode == SanitationMode.rm_update_date:   # reset the -updatedAt- field
            dto.updatedAt = None
        if mode == SanitationMode.rm_create_date:   # reset the -createdAt- field
            dto.createdAt = None

    @staticmethod
    def __id_sanitation(dto: Union[EntityM, Entity]):
        if hasattr(dto, 'id'): delattr(dto, 'id')



    async def get_all(self) -> List[Catalog]:
        """
        Retrieve all catalog from the database

        :return: List of catalogs
        """
        catalogs: List = []

        async for catalog in self.catalogs_db.find():
            catalogs.append(Catalog(**catalog))

        return catalogs

    async def get(self, catalog_object_id: ObjectId) -> Union[None, Catalog]:
        """
        Get a specific catalog and try to find it

        :return: The catalog to find or None if ir's missing
        """

        db_catalog = await self.catalogs_db.find_one({"_id": catalog_object_id})

        if db_catalog: return Catalog(**db_catalog)
        else: return None

    async def create(self, catalog_dto: Catalog) -> Union[bool, InsertOneResult]:
        """
        Created a new catalog in to the database

        :param catalog_dto: The Catalog to be added
        :return: The new added already catalog object
        """

        catalog_dto.createdAt = datetime.utcnow()
        self.__id_sanitation(catalog_dto)                                                          # if the dto has id, we remove it
        self.__date_sanitation(SanitationMode.rm_update_date, catalog_dto)                         # Update date sanitation

        try: q_result: InsertOneResult = await self.catalogs_db.insert_one(catalog_dto.dict(by_alias = True))
        except: return False

        return q_result

    async def update(self, catalog_dto: Catalog) -> Union[bool, UpdateResult]:

        self.__date_sanitation(SanitationMode.rm_create_date, catalog_dto)                         # Update date sanitation
        catalog_dto.updatedAt = datetime.utcnow()

        try: q_result: UpdateResult = await self.catalogs_db.update_one(
            {"_id": catalog_dto.id},
            {"$set": catalog_dto.dict(by_alias = True, exclude_none = True)})
        except: return False

        return q_result

    async def delete(self, catalog_object_id: ObjectId) -> Union[None, bool, Catalog]:
        catalog_db = await self.catalogs_db.find_one({"_id": catalog_object_id})

        if catalog_db:
            try: await self.catalogs_db.delete_one({"_id": catalog_object_id})
            except: return False                         # something was wrong
        else: return None                                # 404

        return Catalog(**catalog_db)

    async def set_status(self, catalog_object_id: ObjectId, new_status: bool) -> Union[bool, UpdateResult]:
        """
        Set a new status for the Catalog, according to the new_status parameter.

        :rtype: Catalog
        """

        try:
            q_result: UpdateResult = await self.catalogs_db.update_one(
                {"_id": catalog_object_id},
                {"$set": {
                    "isEnable":  new_status,
                    "updatedAt": datetime.utcnow()
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
            q_result = await self.catalogs_db.update_many(
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

        try: q_result: DeleteResult = await self.catalogs_db.delete_many({"_id": {"$in": ids}})
        except: return False

        return True if q_result.deleted_count > 0 else None
