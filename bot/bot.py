import asyncio
import aiohttp
import os
from dotenv import load_dotenv
import json

# Загрузка переменных окружения
load_dotenv()

# Константы
VK_API_URL = "https://api.vk.com/method/"
VK_TOKEN = os.getenv('VK_TOKEN')
API_VERSION = "5.131"

async def send_message(session, user_id, message):
    """Асинхронная отправка сообщения пользователю"""
    params = {
        "user_id": user_id,
        "message": message,
        "random_id": 0,
        "access_token": VK_TOKEN,
        "v": API_VERSION
    }
    async with session.get(f"{VK_API_URL}messages.send", params=params) as response:
        return await response.json()

async def get_updates(session, ts):
    """Получение обновлений через Long Poll"""
    params = {
        "access_token": VK_TOKEN,
        "v": API_VERSION,
        "act": "a_check",
        "key": "",
        "ts": ts,
        "wait": 25
    }
    
    # Получаем сервер для Long Poll
    async with session.get(f"{VK_API_URL}messages.getLongPollServer", params=params) as response:
        server_data = await response.json()
        server = server_data["response"]
        
        params = {
            "act": "a_check",
            "key": server["key"],
            "ts": server["ts"],
            "wait": 25
        }
        
        async with session.get(f"https://{server['server']}", params=params) as response:
            return await response.json()

async def main():
    """Основной асинхронный цикл бота"""
    print("Асинхронный бот запущен")
    async with aiohttp.ClientSession() as session:
        ts = 0
        while True:
            try:
                updates = await get_updates(session, ts)
                ts = updates["ts"]
                
                for update in updates.get("updates", []):
                    if update[0] == 4:  # Новое сообщение
                        user_id = update[3]
                        # Получаем текст сообщения из правильного индекса
                        text = update[6].lower() if len(update) > 6 else ""
                        
                        print(f"Получено сообщение: {text}")  # Добавляем логирование
                        
                        if text == "начать":
                            await send_message(session, user_id, "Привет! Я асинхронный бот ВКонтакте!")
                            print("Отправлено приветственное сообщение")  # Добавляем логирование
                        else:
                            await send_message(session, user_id, f"Вы написали: {text}")
                            
            except Exception as e:
                print(f"Ошибка: {e}")
                await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())

