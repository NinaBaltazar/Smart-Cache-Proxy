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
	@echo "Populando cache com algumas URLs..."
	# Primeira rodada - MISS
	curl -s http://localhost:5001/example.com > /dev/null
	curl -s http://localhost:5001/jsonplaceholder.typicode.com/posts/1 > /dev/null
	curl -s http://localhost:5001/loripsum.net/api/3 > /dev/null

	# Segunda rodada - HITS (porque já estão em cache)
	curl -s http://localhost:5001/example.com > /dev/null
	curl -s http://localhost:5001/jsonplaceholder.typicode.com/posts/1 > /dev/null
	curl -s http://localhost:5001/loripsum.net/api/3 > /dev/null

	@echo "Feito! Vá para http://localhost:5001/status"

reload:
	make down
	make build
	make up

