from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from app.core.module_loader import ModuleLoader
from app.core.selenium_manager import SeleniumManager
from app.core.config import settings

app = FastAPI(title="Selenium Agent Server")
selenium_manager = SeleniumManager()
module_loader = ModuleLoader()

@app.on_event("startup")
async def startup():
    # Initialize Redis cache
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# Load all modules
module_loader.discover_and_load_modules()

# Include all module routers
for router in module_loader.get_all_routers():
    app.include_router(router)

# You can add global middleware, error handlers, etc. here 