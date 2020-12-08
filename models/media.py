from typing import Optional, List, Set
from datetime import datetime
from enum import Enum

from models.entity import EntityM, DateEntity
from pydantic import Field


class FilmGenre(Enum):
    default = 'default'
    drama = 'drama'
    action = 'action'
    scifi = 'science fiction'
    animation = 'animation'


class GameGenre(Enum):
    default = 'default'
    rpg = 'rpg'
    platform = 'platform'
    detective = 'detective'
    graphic_adventure = 'graphic adventure'
    rts = 'rts'
    simulation = 'simulation'
    moba = 'moba'



class Media(EntityM, DateEntity):
    # TODO POSTER field. When upload a file image, cropped it to several sizes. You have to maintains the original in the physical folder for manual copy
    name: str                       = Field(description = "Name of the media folder", max_length = 60)
    physicalName: str               = Field(description = "The real / filesystem name of the source")
    src: str                        = Field(description = "The path source to the media")
    isEnable: bool                  = Field(description = "If the media is enable", default = True)
    description: Optional[str]      = Field(description = "On optional description")
    released: Optional[datetime]    = Field(description = "Release date of the media")
    price: int                      = Field(description = "Integer representation of the price of the media")
    size: int                       = Field(description = "Integer representation of the size in MB")
    folders: Optional[List[str]]    = Field(description = "List of children folders")
    # FIXME I think we need to have a enum genre for generic media.
    # thing we need to have a table for entity-type / categories and relate to each entity-type / categories the kind of processing, remember one catalog one entity-type / category
    # This could represent seasons of a series


class Film(Media):
    Director: Optional[str]         = Field(description = "The director of the movie", max_length = 30)
    genre: Optional[Set[str]]       = Field(description = "The category of the movie", default = {FilmGenre.default})
    synopsis: Optional[str]         = Field(description = "An overview", max_length = 250)
    trailer: Optional[str]          = Field()


class Game(Media):
    Director: Optional[str]         = Field(description = "The studio of the game", max_length = 30)
    Publisher: Optional[str]        = Field(description = "The publisher company of the game", max_length = 30)
    genre: Optional[Set[str]]       = Field(description = "The category of the game", default = {GameGenre.default})
    trailer: Optional[str]          = Field()
    gameplay: Optional[str]         = Field(description = "Gameplay video src path")
    # TODO SCREENSHOTS field. When upload a file image, cropped it to several sizes. You have to maintains the original in the physical folder for manual copy
