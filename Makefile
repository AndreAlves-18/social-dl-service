rebuild:
	docker stop meu-downloader && docker rm meu-downloader && docker build -t social-dl . && docker run -d -p 8001:8000 --name meu-downloader --restart always social-dl

rm:
	docker stop meu-downloader && docker rm meu-downloader 