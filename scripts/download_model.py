from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_NAME = "RUSpam/spamNS_v1"

AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=1)
AutoTokenizer.from_pretrained(MODEL_NAME)
