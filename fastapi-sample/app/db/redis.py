import redis.asyncio as redis
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger()


class RedisClient:

    _client: redis.Redis | None = None

    @classmethod
    async def connect(cls):

        if cls._client is None:
            try:
                cls._client = redis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True
                )

                await cls._client.ping()

                logger.info("redis.py => connect() => Connected to Redis")

            except Exception as e:
                logger.error(f"redis.py => connect() => Failed to connect: {e}")
                raise

    @classmethod
    def get_client(cls):

        if cls._client is None:
            raise RuntimeError("Redis not initialized")

        return cls._client

    @classmethod
    async def close(cls):

        if cls._client:
            await cls._client.close()
            logger.info("redis.py => close() => Redis connection closed")