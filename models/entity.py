from .pyObjectId import PyObjectId
from datetime import datetime
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field


class DateEntity(BaseModel):
    createdAt: Optional[datetime] = Field(description="DateTime for the creation instant of the entity")
    updatedAt: Optional[datetime] = Field(description="DateTime for the update instant of the entity")


class Entity(BaseModel):
    """
    General purpose base entity from Pydantic
    """
    id: int = Field(description="The unique Id of the entity", ge=0)


class EntityM(BaseModel):
    """
    General purpose MongoDB compatible, base entity from Pydantic
    """
    id: Optional[PyObjectId] = Field(alias='_id')                       # If no Id present, assume to be a new entity

    class Config:
        arbitrary_types_allowed = True                                  # Here we tell Pydantic that we are using a custom type
        json_encoders = {ObjectId: str}                                 # Mapping for JSON serialization
