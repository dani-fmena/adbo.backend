import motor.motor_asyncio
from pymongo.database import Database
from config.config import CONFIGS


_client = motor.motor_asyncio.AsyncIOMotorClient(CONFIGS.MONGO_DETAILS)
db: Database = _client.adbo
