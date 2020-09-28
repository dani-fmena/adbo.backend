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

    @staticmethod
    def __db_collection():
        return db.get_collection("catalogs")

    @staticmethod
    def __date_sanitation(mode: Enum, dto: Union[DateEntity]):
        if mode == SanitationMode.rm_both_date:
            dto.createdAt = None
            dto.updatedAt = None
        if mode == SanitationMode.rm_update_date:
            dto.updatedAt = None
        if mode == SanitationMode.rm_create_date:
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
    async def get(catalog_id: str) -> Union[None, Catalog]:
        """
        Get a specific catalog and try to find it

        :return: The catalog to find or None if ir's missing
        """
        collection = CatalogDB.__db_collection()
        new_catalog = await collection.find_one({"_id": ObjectId(catalog_id)})

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
        CatalogDB.__id_sanitation(catalog_dto)  # if the dto has id, we remove it
        CatalogDB.__date_sanitation(SanitationMode.rm_update_date, catalog_dto)                         # Update date sanitation

        q_result = await collection.insert_one(catalog_dto.dict(by_alias=True))
        new_catalog = await collection.find_one({"_id": q_result.inserted_id})

        return Catalog(**new_catalog)

    @staticmethod
    async def update(catalog_dto: Catalog) -> Union[None, Catalog]:
        collection = CatalogDB.__db_collection()
        q_result = collection.find_one({"_id": catalog_dto.id})

        if q_result:
            CatalogDB.__date_sanitation(SanitationMode.rm_create_date, catalog_dto)                     # Update date sanitation
            catalog_dto.updatedAt = datetime.utcnow()

            await collection.update_one({"_id": catalog_dto.id}, {"$set": catalog_dto.dict(by_alias=True, exclude_none=True)})
            catalog_db = await collection.find_one({"_id": catalog_dto.id})

            return Catalog(**catalog_db)
        else: return None


    @staticmethod
    async def delete(catalog_id: str) -> Union[None, Catalog]:
        collection = CatalogDB.__db_collection()
        catalog_db = await collection.find_one({"_id": ObjectId(catalog_id)})

        if catalog_db:
            await collection.delete_one({"_id": ObjectId(catalog_id)})
            return Catalog(**catalog_db)
        else: return None
