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

clean:
	docker-compose down -v --remove-orphans
