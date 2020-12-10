from enum import Enum
from typing import Union
from pymongo.collection import Collection
from api.db_session import db
from models.entity import EntityM, Entity, DateEntity


class SanitationMode (Enum):
    rm_create_date = 1
    rm_update_date = 2
    rm_both_date = 3


class BaseDB:
    """
    Database access related to the catalog entity
    """
    collection: Collection

    def __init__(self, db_collection_name: str):
        self.collection = db.get_collection(db_collection_name)

    def date_sanitation(self, mode: SanitationMode, dto: Union[DateEntity]):
        """
        Depending of the parameter, we reset the corresponding date field in the DTO, so the DTO dont
        inject 'noise' and 'dirt' to the database.

        :rtype: None
        """
        if mode == SanitationMode.rm_both_date:  # reset the -createdAt- and -createdAt- field
            dto.createdAt = None
            dto.updatedAt = None
        if mode == SanitationMode.rm_update_date:  # reset the -updatedAt- field
            dto.updatedAt = None
        if mode == SanitationMode.rm_create_date:  # reset the -createdAt- field
            dto.createdAt = None

    def id_sanitation(self, dto: Union[EntityM, Entity]):
        if hasattr(dto, 'id'): delattr(dto, 'id')

