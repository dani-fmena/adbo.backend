from typing import List, Union
from models.catalog import Catalog
from .base_serv import BaseService
from repository.db.catalog_db import CatalogDB
from services.helpers import chunker
from config.config import CONFIGS


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

    async def create(self, catalog_dto: Catalog) -> Union[None, Catalog]:
        op_result = await CatalogDB.create(catalog_dto)

        if op_result is False: self.RiseHTTP_DataLayerFail()
        else: return await CatalogDB.get(op_result.inserted_id)

    async def update(self, catalog_dto: Catalog) -> Union[None, Catalog]:
        op_result = await CatalogDB.update(catalog_dto)

        if op_result is False: self.RiseHTTP_DataLayerFail()
        elif op_result.matched_count == 0: self.RiseHTTP_NotFound()
        elif op_result.modified_count == 0: self.RiseHTTP_DataLayerEmptyOps()

        return await CatalogDB.get(catalog_dto.id)

    async def delete(self, catalog_id: str) -> Union[None, Catalog]:
        object_id_dto = self.chk_object_id(catalog_id)
        result_db = await CatalogDB.delete(object_id_dto)

        if result_db is False: self.RiseHTTP_DataLayerFail()
        elif result_db is None: self.RiseHTTP_NotFound()
        else: return result_db

    async def set_status (self, catalog_id: str, new_status: bool) -> Union[None, bool]:
        object_id_dto = self.chk_object_id(catalog_id)
        op_result = await CatalogDB.set_status(object_id_dto, new_status)

        if op_result is False: self.RiseHTTP_DataLayerFail()
        elif op_result.matched_count == 0: self.RiseHTTP_NotFound()
        elif op_result.modified_count == 0: self.RiseHTTP_DataLayerEmptyOps()
        else: return True

    async def bulk_set_status (self, catalog_ids: List[str], new_status: bool) -> bool:

        for sub_section_ids in chunker(catalog_ids, CONFIGS.CHUNK_SIZE):
            subsection_bson_ids = self.chk_object_ids_list(sub_section_ids)
            op_result = await CatalogDB.bulk_set_status(subsection_bson_ids, new_status)

            if op_result is False: self.RiseHTTP_DataLayerFail()
            elif op_result.matched_count == 0: self.RiseHTTP_NotFound()
            elif op_result.modified_count == 0: self.RiseHTTP_DataLayerEmptyOps()

        return True

    async def bulk_remove (self, catalog_ids: List[str]) -> bool:

        for sub_section_ids in chunker(catalog_ids, CONFIGS.CHUNK_SIZE):
            subsection_bson_ids = self.chk_object_ids_list(sub_section_ids)
            op_result = await CatalogDB.bulk_remove(subsection_bson_ids)                                          # operations result == op_result

            if op_result is False: self.RiseHTTP_DataLayerFail()
            if op_result is None: self.RiseHTTP_NotFound()

        return True
