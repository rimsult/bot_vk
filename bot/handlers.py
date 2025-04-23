from api import VKAPI
from cache import get_cached, set_cached
from storage import Storage

storage = Storage()

async def handle_message(vk: VKAPI, user_id: int, text: str):
    # Логируем входное сообщение
    print(f"Handling message for user {user_id}: '{text}'")

    # Пробуем получить из кэша
    key = f"resp:{text}"
    cached = await get_cached(key)
    if cached:
        return cached

    # Нормализация текста
    cmd = text.strip()

    # Обработка команд для приветствия
    if cmd in ("начать", "привет", "/start"):
        resp = "Привет! Я асинхронный бот ВКонтакте!"
    else:
        resp = f"Вы написали: {text}"

    # Сохраняем в историю и кэшируем
    storage.add_record(user_id, text, resp)
    print(f"Сохранено в историю: {user_id} → '{text}' → '{resp}'")
    await set_cached(key, resp, ttl=120)
    return resp
