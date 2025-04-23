import asyncio
import aiohttp
from api import VKAPI
from handlers import handle_message

async def main():
    print("Запуск бота ...")
    async with aiohttp.ClientSession() as session:
        vk = VKAPI(session)
        server_url, key, ts = await vk.get_longpoll_server()

        while True:
            try:
                resp = await vk.longpoll(server_url, key, ts)

                # Handle VK Long Poll failures
                if isinstance(resp, dict) and resp.get('failed'):
                    code = resp['failed']
                    print(f"LongPoll failed={code}")
                    if code in (2, 3):
                        server_url, key, ts = await vk.get_longpoll_server()
                        continue
                    elif code == 1:
                        ts = resp.get('ts', ts)
                        continue

                # Update ts and process events
                ts = resp.get('ts', ts)
                updates = resp.get('updates', [])

                print(f"Получено обновлений: {len(updates)}")
                for event in updates:
                    if isinstance(event, list) and event[0] == 4:
                        flags = event[2]
                        if flags & 2:  # Пропускаем исходящие сообщения
                            continue

                        user_id = event[3]
                        text = str(event[5]).lower() if len(event) > 5 and isinstance(event[5], str) else ""
                        print(f"Получено сообщение: {text}")
                        response = await handle_message(vk, user_id, text)
                        await vk.send("messages.send", {"user_id": user_id, "message": response, "random_id": 0})

            except Exception as e:
                print(f"Ошибка в цикле: {e}")
                await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())




