from logging.config import dictConfig
from teamiclink.slack.views import register_views
from teamiclink.slack.commands import register_commands

import psycopg2.extras
import yaml
from flask import Flask
from redis import Redis
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt.oauth.oauth_settings import OAuthSettings

from teamiclink.config import AppConfig
from teamiclink.slack.events import register_events
from teamiclink.slack.middleware import SlackMiddleware
from teamiclink.slack.oauth_flow import TeamiclinkOAuth
from teamiclink.slack.store_install import TeamiclinkInstallStore
from teamiclink.slack.store_state import RedisOAuthStateStore
from teamiclink.slack.flask import register_url_rules

psycopg2.extras.register_uuid()

config = AppConfig()

with open(config.path_logging_config, mode="r") as logging_config:
    dictConfig(yaml.safe_load(logging_config.read()))


installation_store = TeamiclinkInstallStore(data_source_name=config.dsn)
slack_handler = SlackRequestHandler(
    app=App(
        signing_secret=config.slack_signing_secret,
        oauth_flow=TeamiclinkOAuth(
            settings=OAuthSettings(
                client_id=config.slack_client_id,
                client_secret=config.slack_client_secret,
                scopes=config.slack_permissions,
                state_store=RedisOAuthStateStore(
                    redis=Redis(
                        host=config.redis_host,
                        port=config.redis_port,
                        db=config.redis_db_install_state,
                        password=config.redis_password,
                        socket_timeout=config.redis_socket_connect_timeout_seconds,
                        socket_connect_timeout=config.redis_socket_connect_timeout_seconds,
                    )
                ),
                installation_store=installation_store,
            )
        ),
    )
)
SlackMiddleware.set_variables(
    install_store=installation_store,
    client_id=config.slack_client_id,
    client_secret=config.slack_client_secret,
)
register_views(app=slack_handler.app, middleware=SlackMiddleware)
register_events(app=slack_handler.app, middleware=SlackMiddleware)
register_commands(app=slack_handler.app, middleware=SlackMiddleware)
app = Flask("teamiclink")
register_url_rules(slack_handler=slack_handler, app=app)
