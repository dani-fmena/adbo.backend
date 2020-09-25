from api.database import db
from models.catalog import Catalog
from typing import List


class CatalogDB:
    """
    Database access related to the catalog entity
    """

    @staticmethod
    async def get_all() -> List[Catalog]:
        """
        Retireve all catalog from the database

        :return: List of catalogs
        """
        catalogs_db = db.get_collection("catalogs")
        catalogs: List = []

        async for catalog in catalogs_db.find():
            catalogs.append(Catalog(**catalog))

        return catalogs

    @staticmethod
    async def create(catalog_dto):
        """
        Created a new catalog in to the database

        :param catalog_dto: The Catalog to be added
        :return: The new added already catalog object
        """
        # if the dto has id, we remove it
        if hasattr(catalog_dto, 'id'): delattr(catalog_dto, 'id')

        catalogs_db = db.get_collection("catalogs")

        q_result = await catalogs_db.insert_one(catalog_dto.dict(by_alias=True))
        new_student = await catalogs_db.find_one({"_id": q_result.inserted_id})

        return Catalog(**new_student)
