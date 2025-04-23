import os
from dotenv import load_dotenv

load_dotenv()

VK_TOKEN = os.getenv("VK_TOKEN")
API_VERSION = "5.131"
VK_API_URL = "https://api.vk.com/method/"

# Limits: requests per second/minute
RATE_LIMIT_PER_SEC = 3
RATE_LIMIT_PER_MIN = 50
