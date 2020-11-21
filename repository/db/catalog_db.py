from pymongo.results import UpdateResult, InsertOneResult, DeleteResult
from pymongo.collection import Collection
from datetime import datetime
from typing import Union, Dict, Any
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

    @staticmethod
    def __db_collection() -> Collection:
        return db.get_collection("catalogs")

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


    @staticmethod
    async def get_all() -> List[Catalog]:
        """
        Retrieve all catalog from the database

        :return: List of catalogs
        """
        collection = CatalogDB.__db_collection()
        catalogs: List = []

        async for catalog in collection.find():
            catalogs.append(Catalog(**catalog))

        return catalogs

    @staticmethod
    async def get(catalog_object_id: ObjectId) -> Union[None, Catalog]:
        """
        Get a specific catalog and try to find it

        :return: The catalog to find or None if ir's missing
        """
        collection = CatalogDB.__db_collection()
        new_catalog = await collection.find_one({"_id": catalog_object_id})

        if new_catalog: return Catalog(**new_catalog)
        else: return None

    @staticmethod
    async def create(catalog_dto: Catalog) -> Catalog:
        """
        Created a new catalog in to the database

        :param catalog_dto: The Catalog to be added
        :return: The new added already catalog object
        """
        collection = CatalogDB.__db_collection()

        catalog_dto.createdAt = datetime.utcnow()
        CatalogDB.__id_sanitation(catalog_dto)                                                          # if the dto has id, we remove it
        CatalogDB.__date_sanitation(SanitationMode.rm_update_date, catalog_dto)                         # Update date sanitation

        q_result: InsertOneResult = await collection.insert_one(catalog_dto.dict(by_alias = True))
        new_catalog = await collection.find_one({"_id": q_result.inserted_id})

        return Catalog(**new_catalog)

    @staticmethod
    async def update(catalog_dto: Catalog) -> Union[None, Catalog]:
        collection = CatalogDB.__db_collection()

        CatalogDB.__date_sanitation(SanitationMode.rm_create_date, catalog_dto)                         # Update date sanitation
        catalog_dto.updatedAt = datetime.utcnow()

        q_result: UpdateResult = await collection.update_one({"_id": catalog_dto.id}, {"$set": catalog_dto.dict(by_alias = True, exclude_none = True)})
        if q_result.modified_count == 0 and q_result.matched_count == 0: return None

        catalog_db = await collection.find_one({"_id": catalog_dto.id})
        return Catalog(**catalog_db)

    @staticmethod
    async def delete(catalog_object_id: ObjectId) -> Union[None, Catalog]:
        collection = CatalogDB.__db_collection()
        catalog_db = await collection.find_one({"_id": catalog_object_id})

        if catalog_db:
            await collection.delete_one({"_id": catalog_object_id})
            return Catalog(**catalog_db)
        else: return None

    @staticmethod
    async def set_status(catalog_object_id: ObjectId, new_status: bool) -> Union[None, bool]:
        """
        Set a new status for the Catalog, according to the new_status parameter.

        :rtype: Catalog
        """
        collection = CatalogDB.__db_collection()

        q_result: UpdateResult = await collection.update_one(
            {"_id": catalog_object_id},
            {"$set": {
                "isEnable":  new_status,
                "updatedAt": datetime.utcnow()
            }}
        )

        if q_result.modified_count == 0 and q_result.matched_count == 0: return None
        return True

    @staticmethod
    async def bulk_enable(ids: List[ObjectId]) -> Union[None, bool]:
        """
        Enable the IDs object in bulk (update_many)

        :param ids:
        :return:
        """
        collection = CatalogDB.__db_collection()
        updated_at = datetime.utcnow()

        q_result: UpdateResult = await collection.update_many(
            {"_id": {"$in": ids}},
            {"$set": {
                "isEnable": True,
                "updatedAt": updated_at
            }}
        )

        return True if q_result else None                                               # Python ternary operator
