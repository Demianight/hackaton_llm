import os

from dotenv import load_dotenv

load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "")

ENABLE_API = os.getenv("ENABLE_API", "false").lower() in ("true", "1", "yes")

BASE_API_URL = os.getenv("BASE_API_URL", "")

ENABLE_AUTO_DELETE = os.getenv("ENABLE_AUTO_DELETE", "false").lower() in (
    "true",
    "1",
    "yes",
)
