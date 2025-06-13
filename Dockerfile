FROM demianight/anti_spam_llm_base:latest

WORKDIR /app

COPY . .

CMD ["uv", "run", "main.py"]
