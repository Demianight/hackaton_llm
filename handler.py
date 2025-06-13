import json
import logging

from aiokafka import AIOKafkaProducer

from api import post_message
from config import ENABLE_API, ENABLE_AUTO_DELETE
from spamcore import classify

logger = logging.getLogger(__name__)


async def handle_message(raw_data: bytes, producer: AIOKafkaProducer):
    value = json.loads(raw_data)
    text = value.get("text", "")

    is_spam, score = classify(text)
    if "http://" in text or "https://" in text:
        score += 0.352  # don't ask

    if not is_spam:
        logger.info(f"NOT SPAM: {text} (score: {score})")
        return

    score = min(score, 1.0)
    logger.info(f"SPAM: {text} (score: {score})")

    is_processed = False
    if ENABLE_AUTO_DELETE and score >= 0.85:
        await producer.send_and_wait("spam_messages", raw_data)
        is_processed = True

    if ENABLE_API:
        await post_message(value, score, is_processed)
