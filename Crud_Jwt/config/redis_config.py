import aioredis


async def get_redis():
    redis = await aioredis.from_url("redis://localhost:6379/1")
    yield redis
    await redis.close()
