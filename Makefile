ENV_FILE=docker.env
DB_PATH_ARG=/src/tcc_poc3.db
include docker.env
export

pipeline:
	# $(MAKE) build
	$(MAKE) psql
	$(MAKE) generate
	$(MAKE) transform
	$(MAKE) load
	$(MAKE) fix
	$(MAKE) ingest
	$(MAKE) patch



# ---------------------- COMMANDS ---------------------- #

measure:
	$(MAKE) get-time
	$(MAKE) get-sizes
get-time:
	sudo make clean; make psql generate; time make transform;
get-sizes:
	echo "Size in Bytes:"
	du -hs -B 1M universidade/data/raw
	du -hs -B 1M universidade/data/curated

build: # BUILDS ALL DOCKER IMAGES NEEDED FOR THE PROJECT
	docker build -t poc3-postgres:latest -f ./docker/postgres.Dockerfile .
	docker build -t poc3-worker:latest -f ./docker/SEAL-Python/Dockerfile .
	docker build -t poc3-duckdb:latest -f ./docker/duckdb.Dockerfile --build-arg DB_PATH_ARG=$(DB_PATH_ARG) .
clean: # REMOVES ALL GENERATED FILES
	docker stop $$(docker ps -f name=poc3 -q) || true
	docker rm -f -v $$(docker ps -f name=poc3 -q) || true
	rm -rf universidade/db/*
	rm -rf postgres/postgres_data
	rm -rf postgres/tls/certs/*
	rm -rf postgres/cert_login/certs/*
	rm -rf $$(find . -type d -name "__pycache__" | xargs)
	rm -rf $$(find . -type f -name "*.json" | xargs)

psql: # STARTS POSTGRES INSTANCE
	chmod +x **/*.sh
	$(MAKE) certificates
	docker compose --env-file $(ENV_FILE) up -d postgres
	sleep 0.5
	./postgres/tls/postgres_conf.sh # TLS
	sleep 0.5
	./postgres/scripts/auditing.sh # PG_AUDIT
	$(MAKE) restart
duckdb: # STARTS DUCKDB INSTANCE AND OPENS DUCKDB CLIENT
	docker compose --env-file $(ENV_FILE) run -v $$(pwd)/universidade/db:/src --rm --name duckdb duckdb $(DB_PATH_ARG)
debug: # STARTS A DEBUG SESSION IN WORKER (PYTHON ENVIRONMENT)
	docker compose --env-file $(ENV_FILE) run -v $$(pwd)/universidade:/src --rm --entrypoint /bin/bash -i -t --name debug worker
standalone-debug: # STARTS A DEBUG SESSION IN WORKER (PYTHON ENVIRONMENT) WITH ROOT PROJECT MOUNTED
	docker run -it --rm --entrypoint bash -v .:/src poc3-worker


generate: # GENERATES RAW DATA
	docker compose --env-file $(ENV_FILE) run -v $$(pwd)/universidade:/src --rm --name generate_data worker generate_data.py
transform: # TRANSFORMS RAW DATA INTO CURATED DATA
	docker compose --env-file $(ENV_FILE) run -v $$(pwd)/universidade:/src --rm --name fhe_keygen worker fhe_keygen.py
	docker compose --env-file $(ENV_FILE) run -v $$(pwd)/universidade:/src --rm --name transform_data worker transform_data.py
load: # INGESTS DATA INTO DUCKDB
	docker compose --env-file $(ENV_FILE) run -v $$(pwd)/universidade:/src --rm --name load_data worker load_data.py
fix: # LOADS DATA FROM DUCKDB TO POSTGRES
	docker compose --env-file $(ENV_FILE) run -v $$(pwd)/postgres:/src/postgres --rm --name duckdb duckdb -no-stdin -init ./postgres/scripts/generate_ids.sql $(DB_PATH_ARG)
	docker compose --env-file $(ENV_FILE) run -v $$(pwd)/postgres:/src/postgres --rm --name duckdb duckdb -no-stdin -init ./postgres/scripts/adequate.sql $(DB_PATH_ARG)
	@echo "${BLUE}Data fixes with DuckDB finished!${END}"
ingest: # INGESTS DATA INTO POSTGRES
	docker compose --env-file $(ENV_FILE) run -v $$(pwd)/universidade:/src --rm --name ingest_data worker ingest_data.py
	@echo "${BLUE}Data ingestion from DuckDB to PostGres finished!${END}"
patch: # MODIFIES DATA IN POSTGRES DATABASE
	# docker compose --env-file $(ENV_FILE) run -v $$(pwd)/universidade:/src --rm --name encrypt_data worker encrypt_data.py
	docker compose --env-file $(ENV_FILE) run -v $$(pwd)/postgres:/src/postgres --rm --name duckdb duckdb -no-stdin -init ./postgres/scripts/pii.sql $(DB_PATH_ARG)
	docker exec $$(docker ps -f name=post -q) psql -U ${PGUSER} -d ${PGDATABASE} -f ./postgres/scripts/constraints.sql
	@echo "${BLUE}Data patching finished!${END}"

restart:
	docker compose --env-file $(ENV_FILE) restart postgres
certificates:
	./postgres/tls/generate_cert.sh
	./postgres/cert_login/generate_user_cert.sh
	mv server.* ./postgres/tls/certs
	mv ca.* ./postgres/tls/certs
	mv consumer.* ./postgres/cert_login/certs
	mv professor.* ./postgres/cert_login/certs








PURPLE = \033[95m
CYAN = \033[96m
DARKCYAN = \033[36m
BLUE = \033[94m
GREEN = \033[92m
YELLOW = \033[93m
RED = \033[91m
BOLD = \033[1m
UNDERLINE = \033[4m
END = \033[0m