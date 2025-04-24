from logger import logger

async def handle_greeting(text: str) -> str:
    logger.info(f"Greeting handler processing: {text}")
    return "Привет! Я асинхронный бот ВКонтакте!"