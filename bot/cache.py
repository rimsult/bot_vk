from aiocache import Cache

# In-memory cache, TTL configurable
cache = Cache(Cache.MEMORY)

async def get_cached(key):
    return await cache.get(key)

async def set_cached(key, value, ttl=60):
    await cache.set(key, value, ttl=ttl)