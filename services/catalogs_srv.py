from typing import List, Union
from models.catalog import Catalog
from repository.db.catalog_db import CatalogDB
from .base_serv import BaseService


class CatalogService(BaseService):
    """"
    Catalog services
    """

    async def get_all(self) -> List[Catalog]:
        return await CatalogDB.get_all()

    async def get_catalog(self, catalog_id: str) -> Union[None, Catalog]:
        result_db = await CatalogDB.get(catalog_id)

        if result_db is None: self.RiseHTTP_NotFound()
        return result_db

    async def create(self, catalog_dto: Catalog) -> Catalog:
        return await CatalogDB.create(catalog_dto)

    async def update(self, catalog_dto: Catalog) -> Union[None, Catalog]:
        result_db = await CatalogDB.update(catalog_dto)

        if result_db is None: self.RiseHTTP_NotFound()
        return result_db

    async def delete(self, catalog_id: str) -> Union[None, Catalog]:
        result_db = await CatalogDB.delete(catalog_id)

        if result_db is None: self.RiseHTTP_NotFound()
        return result_db
