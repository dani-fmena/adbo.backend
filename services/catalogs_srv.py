from typing import List, Union
from models.catalog import Catalog
from repository.db.catalog_db import CatalogDB
from .base_serv import BaseService
from services.helpers import chunker


class CatalogService(BaseService):
    """"
    Catalog services
    """

    async def get_all(self) -> List[Catalog]:
        return await CatalogDB.get_all()

    async def get_catalog(self, catalog_id: str) -> Union[None, Catalog]:
        object_id_dto = self.chk_object_id(catalog_id)
        result_db = await CatalogDB.get(object_id_dto)

        if result_db is None: self.RiseHTTP_NotFound()
        return result_db

    async def create(self, catalog_dto: Catalog) -> Catalog:
        return await CatalogDB.create(catalog_dto)

    async def update(self, catalog_dto: Catalog) -> Union[None, Catalog]:
        result_db = await CatalogDB.update(catalog_dto)

        if result_db is None: self.RiseHTTP_NotFound()
        return result_db

    async def delete(self, catalog_id: str) -> Union[None, Catalog]:
        object_id_dto = self.chk_object_id(catalog_id)
        result_db = await CatalogDB.delete(object_id_dto)

        if result_db is None: self.RiseHTTP_NotFound()
        return result_db

    async def set_status (self, catalog_id: str, new_status: bool) -> Union[None, bool]:
        object_id_dto = self.chk_object_id(catalog_id)
        result_db = await CatalogDB.set_status(object_id_dto, new_status)

        if result_db is None: self.RiseHTTP_NotFound()
        return True

    async def bulk_enable (self, catalog_ids: List[str]) -> Union[None, bool]:

        for sub_section_ids in chunker(catalog_ids, 1000):                                          # the number chunk the input data to try to process it by chunks
            subsection_bson_ids = self.chk_object_ids_list(sub_section_ids)
            if await CatalogDB.bulk_enable(subsection_bson_ids) is None: return False

        return True
