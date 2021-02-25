MIGRATOR := migrate/migrate:v4.13.0
LOCAL_DB_URI := postgres://postgres:postgres@local-db:5432/main_db?sslmode=disable
VERSION := 1.1.0

.PHONY: create_migration
create_migration:
	docker run \
		-v ${PWD}:/root/sources \
		-w /root/sources \
		--rm ${MIGRATOR} \
		create -ext sql -dir ./migrations -seq ${Name}

.PHONY: db
db:
	make start_db_local migrate_db_local_up

.PHONY: undb
undb:
	make migrate_db_local_down stop_db_local

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
	timeout 15s bash -c \
		'until docker exec local-db pg_isready; do sleep 1; done'

.PHONY: stop_db_local
stop_db_local:
	docker container stop local-db
	docker network rm local-db-net

.PHONY: migrate_db_local_up
migrate_db_local_up:
	docker run \
		-v ${PWD}/migrations:/migrations \
		--net local-db-net \
		--rm ${MIGRATOR} \
		-database ${LOCAL_DB_URI} \
		-source=file://migrations up

.PHONY: migrate_db_local_down
migrate_db_local_down:
	docker run \
		-v ${PWD}/migrations:/migrations \
		--net local-db-net \
		--rm ${MIGRATOR} \
		-database ${LOCAL_DB_URI} \
		-source=file://migrations down -all


.PHONY: lint
lint:
	flake8 teamiclink test
	black teamiclink test --check
	mypy -p teamiclink

.PHONY: format_migrations
format_migrations:
	find ./migrations -type f -name '*.sql' \
	-type f -exec pg_format --no-extra-line --inplace {} \;

.PHONY: test
test:
	pytest -v --cov teamiclink

.PHONY: docker
docker:
	docker build -t registry.gitlab.com/registry-docker/teamiclink:${VERSION} .

.PHONY: docker_push
docker_push:
	docker push registry.gitlab.com/registry-docker/teamiclink:${VERSION}
