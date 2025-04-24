from logger import logger

async def handle_echo(text: str) -> str:
    logger.info(f"Echo handler processing: {text}")
    return f"Вы написали: {text}"