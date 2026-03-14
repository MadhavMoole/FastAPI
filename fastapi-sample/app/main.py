from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logger import get_logger
from app.core.middleware import RequestLoggingMiddleware

from app.db.mongo import MongoDB
from app.db.redis import RedisClient


logger = get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("main.py => lifespan() => Application startup initiated")

    try:
        MongoDB.connect()
        await RedisClient.connect()

        logger.info("main.py => lifespan() => MongoDB and Redis connections established")

    except Exception as e:
        logger.error(f"main.py => lifespan() => Startup failure: {e}")
        raise

    yield

    logger.info("main.py => lifespan() => Application shutdown initiated")

    try:
        MongoDB.close()
        await RedisClient.close()

        logger.info("main.py => lifespan() => MongoDB and Redis connections closed")

    except Exception as e:
        logger.error(f"main.py => lifespan() => Shutdown error: {e}")


app = FastAPI(
    title="FastAPI Production API",
    version="1.0.0",
    description="FastAPI + MongoDB + Redis Boilerplate",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "FastAPI backend running",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    logger.info("main.py => health_check() => Health endpoint called")
    return { "status": "ok" }