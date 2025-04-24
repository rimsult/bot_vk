from api import VKAPI
from cache import get_cached, set_cached
from storage import Storage
from handlers.greeting import handle_greeting
from handlers.echo import handle_echo
from logger import logger

storage = Storage()

async def route_message(vk: VKAPI, user_id: int, text: str) -> str:
    logger.info(f"Received message from {user_id}: '{text}'")
    text_norm = text.strip().lower()
    key = f"resp:{text_norm}"

    # Check cache
    cached = await get_cached(key)
    if cached:
        logger.debug(f"Cache hit for '{text_norm}' -> '{cached}'")
        storage.add_record(user_id, text_norm, cached)
        return cached

    # Route to handler
    if text_norm in ("начать", "привет", "/start"):
        resp = await handle_greeting(text_norm)
    else:
        resp = await handle_echo(text_norm)

    # Save and cache
    storage.add_record(user_id, text_norm, resp)
    await set_cached(key, resp, ttl=120)
    logger.info(f"Responding to {user_id}: '{resp}'")
    return resp

