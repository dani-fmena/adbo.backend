from models.entity import EntityM
from pydantic import Field


class Catalog(EntityM):
    name: str = Field(description="The name of the Catalog", max_length=30)
