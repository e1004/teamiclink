MIGRATOR := migrate/migrate:v4.13.0
LOCAL_DB_URI := postgres://postgres:postgres@local-db:5432/main_db?sslmode=disable

.PHONY: create_migration
create_migration:
	docker run \
		-v ${PWD}:/root/sources \
		-w /root/sources \
		--rm ${MIGRATOR} \
		create -ext sql -dir ./migrations -seq ${Name}

.PHONY: start_db_local
start_db_local:
	docker network create local-db-net
	docker run --rm --name local-db \
		-p 5432:5432 -d \
		--net local-db-net \
		-e POSTGRES_USER=postgres \
		-e POSTGRES_PASSWORD=postgres \
		-e POSTGRES_DB=main_db \
		postgres:13.0-alpine -c "fsync=off"

.PHONY: stop_db_local
stop_db_local:
	docker container stop local-db
	docker network rm local-db-net

.PHONY: migrate_db_local_up
migrate_db_local_up:
	docker run \
		-v ${PWD}:/root/sources \
		-v ${PWD}/migrations:/migrations \
		-w /root/sources \
		--net local-db-net \
		--rm ${MIGRATOR} \
		-database ${LOCAL_DB_URI} \
		-path ./migrations up

.PHONY: migrate_db_local_down
migrate_db_local_down:
	docker run \
		-v ${PWD}:/root/sources \
		-v ${PWD}/migrations:/migrations \
		-w /root/sources \
		--net local-db-net \
		--rm ${MIGRATOR} \
		-database ${LOCAL_DB_URI} \
		-path ./migrations down -all

.PHONY: test
test:
	pytest

.PHONY: lint
lint:
	flake8 upt test
	black upt test --check
	mypy -p upt
