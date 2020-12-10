import motor.motor_asyncio
from pymongo.database import Database
from config.config import CONFIGS


client = motor.motor_asyncio.AsyncIOMotorClient(CONFIGS.MONGO_DETAILS)
db: Database = client.adbo


