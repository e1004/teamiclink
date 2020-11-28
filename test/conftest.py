from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock

import pytest
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt.app import App
from upt.app import create_app
from upt.database import Database

DB = {
    "host": "localhost",
    "port": "5432",
    "dbname": "main_db",
    "user": "robot",
    "password": "any_password_replaced_later",
}

DB_USER_REGULAR = (
    f"postgres://{DB['user']}:"
    f"{DB['password']}@"
    f"{DB['host']}:"
    f"{DB['port']}/"
    f"{DB['dbname']}?sslmode=disable"
)

DB_USER_ROOT = (
    "postgres://postgres:"
    "postgres@"
    f"{DB['host']}:"
    f"{DB['port']}/"
    f"{DB['dbname']}?sslmode=disable"
)


@pytest.fixture(scope="session")
def create_db_cleaner():
    "https://gist.github.com/mayank-io/6c492cf53a546773650c"
    with Database.connect(data_source_name=DB_USER_ROOT) as connection:
        with Database.create_cursor(connection=connection) as cursor:
            cursor.execute(
                """
                    CREATE OR REPLACE FUNCTION clean_tables()
                    RETURNS void AS
                    $func$
                    BEGIN
                        EXECUTE 'TRUNCATE TABLE '
                        || string_agg(quote_ident(schemaname) || '.' || quote_ident(tablename), ', ')
                        || ' CASCADE;'
                        FROM   pg_tables
                        WHERE  schemaname = 'upt';
                    END
                    $func$ LANGUAGE plpgsql;
                """
            )


@pytest.fixture
def clean_db(create_db_cleaner):
    yield
    with Database.connect(data_source_name=DB_USER_ROOT) as connection:
        with Database.create_cursor(connection=connection) as cursor:
            cursor.execute("SELECT clean_tables()")


@dataclass
class Target:
    client: Any
    slack_handler: SlackRequestHandler


@pytest.fixture
def target():
    slask_app = MagicMock(spec=App)
    slack_handler = SlackRequestHandler(app=slask_app)
    app = create_app(slack_handler=slack_handler)
    app.testing = True
    with app.test_client() as client:
        yield Target(client=client, slack_handler=slack_handler)
