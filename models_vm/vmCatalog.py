from models.entity import EntityM, DateEntity
from pydantic import Field


class CatalogIn:
    name: str = Field(description='The name of the Catalog', max_length=30)
