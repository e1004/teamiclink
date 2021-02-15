from dataclasses import dataclass
from teamiclink.slack.store_goal import GoalStore
from typing import Any
from unittest.mock import MagicMock

import pytest
from flask import Flask
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt.app import App
from teamiclink.database import Database
from teamiclink.slack.flask import register_url_rules
from teamiclink.slack.middleware import SlackMiddleware
from teamiclink.slack.store_install import TeamiclinkInstallStore
import psycopg2.extras

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
                        WHERE  schemaname = 'teamiclink';
                    END
                    $func$ LANGUAGE plpgsql;
                """
            )


@pytest.fixture
def clean_db(create_db_cleaner):
    psycopg2.extras.register_uuid()
    yield
    with Database.connect(data_source_name=DB_USER_ROOT) as connection:
        with Database.create_cursor(connection=connection) as cursor:
            cursor.execute("SELECT clean_tables()")


@dataclass
class Target:
    client: Any
    slack_handler: SlackRequestHandler
    slack_middleware: SlackMiddleware
    install_store: TeamiclinkInstallStore


@pytest.fixture
def target():
    slask_app = App(
        name="teamiclink", token_verification_enabled=False, token="any_token"
    )
    slack_handler = SlackRequestHandler(app=slask_app)
    goal_store = MagicMock(spec=GoalStore)
    install_store = MagicMock(spec=TeamiclinkInstallStore)
    SlackMiddleware.set_variables(
        goal_store=goal_store,
        install_store=install_store,
        client_id="any_client_id",
        client_secret="any_client_secret",
    )
    app = Flask("teamiclink")
    register_url_rules(slack_handler=slack_handler, app=app)
    app.testing = True
    with app.test_client() as client:
        yield Target(
            client=client,
            slack_handler=slack_handler,
            slack_middleware=SlackMiddleware,
            install_store=install_store,
        )
