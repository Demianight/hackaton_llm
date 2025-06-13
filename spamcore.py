import re

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_NAME = "RUSpam/spamNS_v1"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = (
    AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=1)
    .to(DEVICE)
    .eval()
)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def clean_text(text: str) -> str:
    text = re.sub(r"[^А-Яа-я0-9 ]+", " ", text)
    return text.lower().strip()


def classify(text: str) -> tuple[bool, float]:
    cleaned = clean_text(text)
    encoding = tokenizer(
        cleaned,
        padding="max_length",
        truncation=True,
        max_length=128,
        return_tensors="pt",
    )

    input_ids = encoding["input_ids"].to(DEVICE)
    attention_mask = encoding["attention_mask"].to(DEVICE)

    with torch.no_grad():
        logits = model(input_ids, attention_mask=attention_mask).logits
        score = torch.sigmoid(logits).cpu().numpy()[0][0]

    return bool(score >= 0.5), float(score)
