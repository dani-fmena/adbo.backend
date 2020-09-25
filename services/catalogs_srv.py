from typing import List
from models.catalog import Catalog
from repository.db.catalog_db import CatalogDB


class CatalogService:
    """"
    Catalog services
    """

    @staticmethod
    async def get_all() -> List[Catalog]:
        return await CatalogDB.get_all()

    @staticmethod
    async def create(catalog_dto) -> Catalog:
        # We can do business logic validation here
        return await CatalogDB.create(catalog_dto)

