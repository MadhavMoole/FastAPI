from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger()


class MongoDB:

    _client: AsyncIOMotorClient | None = None
    _db = None

    @classmethod
    def connect(cls):

        if cls._client is None:
            try:
                cls._client = AsyncIOMotorClient(settings.MONGO_URL)
                cls._db = cls._client[settings.DB_NAME]

                logger.info("mongo.py => Connected to MongoDB")

            except Exception as e:
                logger.error(f"mongo.py => Failed to connect: {e}")
                raise

    @classmethod
    def get_db(cls):

        if cls._db is None:
            raise RuntimeError("MongoDB not initialized")

        return cls._db

    @classmethod
    def close(cls):

        if cls._client:
            cls._client.close()
            logger.info("mongo.py => MongoDB connection closed")