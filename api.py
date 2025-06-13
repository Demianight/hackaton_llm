import logging

from httpx import AsyncClient
from httpx_retries import Retry, RetryTransport

from config import BASE_API_URL

retry = Retry(total=5, backoff_factor=0.5)
transport = RetryTransport(retry=retry)

logger = logging.getLogger()


async def post_message(message: dict, score: float, is_processed: bool):
    async with AsyncClient(transport=transport) as client:
        client.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = await client.post(
            f"{BASE_API_URL}/messages/",
            json={"spam_score": score, "is_processed": is_processed, **message},
        )
        logger.info(f"Posted message to API: {response.status_code} - {response.text}")
