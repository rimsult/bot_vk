import aiohttp
from aiolimiter import AsyncLimiter
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from config import VK_API_URL, VK_TOKEN, API_VERSION, RATE_LIMIT_PER_SEC, RATE_LIMIT_PER_MIN
from logger import logger

# Rate limiter: X requests/sec, Y requests/min
limiter_sec = AsyncLimiter(RATE_LIMIT_PER_SEC, 1)
limiter_min = AsyncLimiter(RATE_LIMIT_PER_MIN, 60)

class VKAPI:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1), retry=retry_if_exception_type(aiohttp.ClientError))
    async def send(self, method: str, params: dict):
        """Generic VK API call"""
        async with limiter_sec, limiter_min:
            params.update({"access_token": VK_TOKEN, "v": API_VERSION})
            url = f"{VK_API_URL}{method}"
            logger.debug(f"VKAPI.send: GET {url} params={params}")
            async with self.session.get(url, params=params) as resp:
                data = await resp.json()
                if 'error' in data:
                    logger.error(f"VK API error: {data['error']}")
                    raise Exception(f"VK API error: {data['error']}")
                return data['response']

    async def get_longpoll_server(self):
        """Get Long Poll server info: full URL, key, ts"""
        resp = await self.send("messages.getLongPollServer", {})
        server = resp.get('server')
        server_url = server if server.startswith('https://') else f"https://{server}"
        return server_url, resp.get('key'), resp.get('ts')

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1), retry=retry_if_exception_type(aiohttp.ClientError))
    async def longpoll(self, server_url: str, key: str, ts: int, wait: int = 25, version: int = 3):
        """Direct Long Poll request to VK server"""
        params = {"act": "a_check", "key": key, "ts": ts, "wait": wait, "version": version}
        logger.debug(f"LongPoll request to {server_url} params={params}")
        async with limiter_sec, limiter_min:
            async with self.session.get(server_url, params=params) as resp:
                result = await resp.json()
                logger.debug(f"LongPoll response: {result}")
                return result