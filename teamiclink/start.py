from logging.config import dictConfig

import psycopg2.extras
import yaml
from redis import Redis
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt.oauth.oauth_settings import OAuthSettings

from teamiclink.app import create_app
from teamiclink.config import AppConfig
from teamiclink.slack.oauth_flow import TeamiclinkOAuth
from teamiclink.slack.store_install import TeamiclinkInstallStore
from teamiclink.slack.store_state import RedisOAuthStateStore

psycopg2.extras.register_uuid()

config = AppConfig.load_from_env()

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
                installation_store_bot_only=True,
            )
        ),
    )
)
app = create_app(slack_handler=slack_handler)
