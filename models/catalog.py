from models.entity import EntityM, DateEntity
from pydantic import Field


class Catalog(EntityM, DateEntity):
    name: str       = Field(description="The name of the Catalog", max_length=30)
    size: int       = Field(description="Total size of the Collection")
    items: int      = Field(description = "Total items in the catalog", default = 0)
    isEnable: bool  = Field(description = "If the catalog is enable", default = True)
