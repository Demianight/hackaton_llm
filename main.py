import asyncio
import logging

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from config import KAFKA_BROKER
from handler import handle_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    consumer = AIOKafkaConsumer(
        "raw_messages",
        bootstrap_servers=KAFKA_BROKER,
        group_id="llm",
        auto_offset_reset="latest",
    )
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)

    await consumer.start()
    await producer.start()
    logger.info("Spam classifier service started.")

    try:
        async for msg in consumer:
            await handle_message(msg.value, producer)
    except asyncio.CancelledError:
        logger.warning("Cancelled by signal.")
        raise
    except Exception:
        logger.exception("Unhandled error in classifier loop")
    finally:
        await consumer.stop()
        await producer.stop()
        logger.info("Kafka clients closed.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Classifier shutdown complete.")
