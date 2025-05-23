build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

logs:
	docker-compose logs -f proxy

bash:
	docker exec -it smartcache-proxy bash

test:
	curl -i http://localhost:5001/example.com

populate:

	curl -s "http://localhost:5001/?url=https://jsonplaceholder.typicode.com/posts/1" > /dev/null
	curl -s "http://localhost:5001/?url=https://jsonplaceholder.typicode.com/posts/1" > /dev/null
	curl -s "http://localhost:5001/?url=http://loripsum.net/api/3" > /dev/null
	curl -s "http://localhost:5001/?url=http://loripsum.net/api/3" > /dev/null
	curl -s "http://localhost:5001/?url=https://example.com" > /dev/null
	curl -s "http://localhost:5001/?url=https://example.com" > /dev/null



reload:
	make down
	make build
	make up

