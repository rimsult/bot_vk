import logging
from logging.handlers import RotatingFileHandler

# Configure root logger
logger = logging.getLogger('vk_bot')
logger.setLevel(logging.DEBUG)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# File handler with rotation
fh = RotatingFileHandler('bot.log', maxBytes=5*1024*1024, backupCount=3)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)