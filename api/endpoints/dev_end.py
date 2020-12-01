import string
import random
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
from api.db_session import db

import pymongo
from pymongo.database import CollectionInvalid
from pymongo.collection import Collection
from repository.db.dbcollections import DBCollections


router = APIRouter()


@router.post("/setup", description = "Setup all the collections and indexes")
async def setup_db():
    # CATALOGS
    # try:
    #     await db.create_collection(DBCollections.CATALOGS)
    # except CollectionInvalid:
    #     raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = DBCollections.CATALOGS + "already exist")

    catalogs_coll: Collection = db.get_collection(DBCollections.CATALOGS)
    catalogs_coll.create_index([("name", pymongo.ASCENDING)])
    return {'msg': 'Database Setup Done'}


@router.post("/seed", description = "Seeds the collections")
async def seed_db():
    lst: List[Dict] = []

    # Catalogs
    catalogs_coll: Collection = db.get_collection(DBCollections.CATALOGS)
    for n in range(100): lst.append(
        {
            "name": ''.join(random.choices(string.ascii_lowercase, k=6)),
            "size": 0,
            "items": 0,
            "isEnable": True if random.choice(range(1, 3)) < 2 else False
        }
    )
    catalogs_coll.insert_many(lst)

    return {'msg': 'Database Seeded'}
