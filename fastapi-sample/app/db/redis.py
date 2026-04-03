import redis.asyncio as redis
import time
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

    @classmethod
    async def blacklist_token(cls, jti: str, exp: int):
        """
        Add token to blacklist until it expires
        """
        client = cls.get_client()

        ttl = exp - int(time.time())
        if ttl <= 0:
            return

        key = f"bl:{jti}"

        try:
            await client.setex(key, ttl, "1")
            logger.info(f"Token blacklisted: {jti}")
        except Exception as e:
            logger.error(f"Failed to blacklist token {jti}: {e}")

    @classmethod
    async def is_blacklisted(cls, jti: str) -> bool:
        """
        Check if token is blacklisted
        """
        client = cls.get_client()

        key = f"bl:{jti}"

        try:
            result = await client.exists(key)
            return result == 1
        except Exception as e:
            logger.error(f"Failed to check blacklist for {jti}: {e}")
            return False