import motor.motor_asyncio
from .utils.definitions import CONFIGS


_client = motor.motor_asyncio.AsyncIOMotorClient(CONFIGS.MONGO_DETAILS)
db = _client.adbo
