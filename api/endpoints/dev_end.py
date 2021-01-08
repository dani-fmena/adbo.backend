import string
import random
import pymongo
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
# from pymongo.results import InsertOneResult
from pymongo.database import CollectionInvalid
from pymongo.collection import Collection
from api.db_session import db, client
from api.utils.crypt import hash_pwd
from dal.db.collections import DBCollections
from api.utils.definition_perms import PG_CATALOG, PG_USERS
from models.rbac import RoleId

router = APIRouter()


@router.post("/setup", description = 'Setup all the collections (tables) and indexes')
async def setup_db():
    await client.drop_database('adbo')

    # region USERS ===============================================================================================
    try:
        await db.create_collection(DBCollections.USERS)
    except CollectionInvalid:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = DBCollections.USERS + 'already exist')

    # indexes
    users_coll: Collection = db.get_collection(DBCollections.USERS)
    await users_coll.create_index([('username', pymongo.ASCENDING)], unique = True)
    # endregion ==================================================================================================

    # region CATALOGS ============================================================================================
    try:
        await db.create_collection(DBCollections.CATALOGS)
    except CollectionInvalid:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = DBCollections.CATALOGS + 'already exist')

    # indexes
    catalogs_coll: Collection = db.get_collection(DBCollections.CATALOGS)
    await catalogs_coll.create_index([('name', 'text')], unique = True)
    # endregion ==================================================================================================

    # region PERMS ===============================================================================================
    try:
        await db.create_collection(DBCollections.ROLES)
        await db.create_collection(DBCollections.PERMS)
    except CollectionInvalid:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = DBCollections.CATALOGS + 'already exist')

    roles_coll: Collection = db.get_collection(DBCollections.ROLES)
    await roles_coll.create_index([('name', pymongo.ASCENDING)], unique = True)

    perms_coll: Collection = db.get_collection(DBCollections.PERMS)
    await perms_coll.create_index([('name', pymongo.ASCENDING)], unique = True)
    await perms_coll.create_index([('group', pymongo.ASCENDING)], unique = False)
    # endregion ==================================================================================================

    return {'msg': 'Database Setup Done'}


@router.post("/seed", description = 'Seeds the collections')
async def seed_db():
    lst: List[Dict] = []

    # region CATALOGS ============================================================================================
    catalogs_coll: Collection = db.get_collection(DBCollections.CATALOGS)
    for n in range(25): lst.append(
        {
            'name': ''.join(random.choices(string.ascii_lowercase, k=6)),
            'size': 0,
            'items': 0,
            'createdAt': datetime.utcnow(),
            'updatedAt': None,
            'isEnable': True if random.choice(range(1, 3)) < 2 else False
        }
    )
    await catalogs_coll.insert_many(lst)
    # endregion ==================================================================================================

    # region PERMS ===============================================================================================
    roles_coll: Collection = db.get_collection(DBCollections.ROLES)
    await roles_coll.insert_one({'name': 'r_admin', 'createdAt': datetime.utcnow(), 'updatedAt': None})
    await roles_coll.insert_one({'name': 'r_worker', 'createdAt': datetime.utcnow(), 'updatedAt': None})
    await roles_coll.insert_one({'name': 'r_client', 'createdAt': datetime.utcnow(), 'updatedAt': None})

    role_dict = RoleId(role = 'r_admin').dict()
    await db.get_collection(DBCollections.PERMS).insert_many([
        # USER PERM
        {'name': PG_USERS.LIST, 'group': PG_USERS.__name__, 'roles': [role_dict]},
        {'name': PG_USERS.VIEW, 'group': PG_USERS.__name__, 'roles': [role_dict]},
        {'name': PG_USERS.CREATE, 'group': PG_USERS.__name__, 'roles': [role_dict]},
        {'name': PG_USERS.EDIT, 'group': PG_USERS.__name__, 'roles': [role_dict]},
        {'name': PG_USERS.DELETE, 'group': PG_USERS.__name__, 'roles': [role_dict]},

        # CATALOGS PERMS
        {'name': PG_CATALOG.LIST, 'group': PG_CATALOG.__name__, 'roles': [role_dict]},
        {'name': PG_CATALOG.VIEW, 'group': PG_CATALOG.__name__, 'roles': [role_dict]},
        {'name': PG_CATALOG.CREATE, 'group': PG_CATALOG.__name__, 'roles': [role_dict]},
        {'name': PG_CATALOG.EDIT, 'group': PG_CATALOG.__name__, 'roles': [role_dict]},
        {'name': PG_CATALOG.DELETE, 'group': PG_CATALOG.__name__, 'roles': [role_dict]}
    ])
    # endregion ==================================================================================================

    # region USERS ===============================================================================================
    users_coll: Collection = db.get_collection(DBCollections.USERS)
    await users_coll.insert_one({
        'username':  'admin',
        'email':     'admin@uno.dos',
        'fullName':  'Im The Admin',
        'pwd':       hash_pwd('secret'),
        'role':      'r_admin',
        'isEnable':  True,
        'createdAt': datetime.utcnow(),
        'updatedAt': None
    })
    # endregion ==================================================================================================

    return {'msg': 'Database Seeded'}
