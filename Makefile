build: 
	docker build -t demianight/anti_spam_llm:latest .
run:
	docker run --name anti_spam_llm demianight/anti_spam_llm
kill:
	docker rm -f anti_spam_llm
push:
	docker push demianight/anti_spam_llm:latest
prod:
	docker buildx build --platform linux/amd64 -t demianight/anti_spam_llm:latest --push .
