import json
import re

import torch
from quixstreams import Application
from sqlmodel import SQLModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from crud import create_message
from db import engine
from message import Message

MODEL_NAME = "RUSpam/spamNS_v1"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = (
    AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, num_labels=1)
    .to(DEVICE)
    .eval()
)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

SQLModel.metadata.create_all(engine)


def clean_text(text):
    text = re.sub(r"[^А-Яа-я0-9 ]+", " ", text)
    text = text.lower().strip()
    return text


def classify_message(message):
    message = clean_text(message)
    encoding = tokenizer(
        message,
        padding="max_length",
        truncation=True,
        max_length=128,
        return_tensors="pt",
    )
    input_ids = encoding["input_ids"].to(DEVICE)
    attention_mask = encoding["attention_mask"].to(DEVICE)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask).logits
        score = torch.sigmoid(outputs).cpu().numpy()[0][0]

    is_spam = int(score >= 0.5)
    return is_spam, float(score)


def main():
    app = Application(
        broker_address="10.10.127.2:9092",
        loglevel="INFO",
        consumer_group="llm",
    )
    with app.get_consumer() as consumer:
        consumer.subscribe(["raw_messages"])

        while True:
            msg = consumer.poll(1)
            if msg is None:
                continue
            elif msg.error() is not None:
                raise Exception(msg.error())

            value = json.loads(msg.value())  # noqa
            text = value["text"]

            is_spam, score = classify_message(text)
            if ("http://" or "https://") in text:
                score += 0.352
            if is_spam:
                if score > 1:
                    score = 1
                message = Message(
                    spam_score=score,
                    **value,
                )
                create_message(message)  # сохраняем в бд
                if score >= 0.7:  # если прям спам спам, то пушим на удаление
                    with app.get_producer() as producer:
                        producer.produce(
                            topic="spam_messages",
                            value=msg.value(),
                        )
                print(f"Message is spam: {text} (score: {score})")
            else:
                print(f"Message is not spam: {text} (score: {score})")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
