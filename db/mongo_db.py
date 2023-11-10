import motor.motor_asyncio
from config.config import settings

MONGO_URI = settings.MONGO_URI
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client[settings.MONGO_DATABASE_NAME]


def get_mongo_db():
    mongo_db = database
    return mongo_db
