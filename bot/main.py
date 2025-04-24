import asyncio
import aiohttp
from api import VKAPI
from router import route_message
from logger import logger

async def main():
    logger.info("Starting VK bot via Direct Long Poll...")
    async with aiohttp.ClientSession() as session:
        vk = VKAPI(session)
        server_url, key, ts = await vk.get_longpoll_server()

        while True:
            try:
                resp = await vk.longpoll(server_url, key, ts)

                # Handle VK Long Poll failures
                if isinstance(resp, dict) and resp.get('failed'):
                    code = resp['failed']
                    logger.warning(f"LongPoll failed={code}")
                    if code in (2, 3):
                        server_url, key, ts = await vk.get_longpoll_server()
                        continue
                    if code == 1:
                        ts = resp.get('ts', ts)
                        continue

                # Update ts and process events
                ts = resp.get('ts', ts)
                updates = resp.get('updates', [])
                logger.debug(f"Poll updates count: {len(updates)}")

                for event in updates:
                    if isinstance(event, list) and event[0] == 4:
                        flags = event[2]
                        if flags & 2:
                            continue
                        user_id = int(event[3])
                        text = str(event[5])
                        logger.info(f"Event msg from {user_id}: {text}")
                        response = await route_message(vk, user_id, text)
                        await vk.send("messages.send", {"user_id": user_id, "message": response, "random_id": 0})

            except Exception as e:
                logger.error(f"Error in loop: {e}")
                await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())

