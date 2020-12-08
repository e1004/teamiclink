from teamiclink.config import AppConfig
from teamiclink.slack.store_install import TeamiclinkInstallStore
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from teamiclink.slack.oauth_flow import TeamiclinkOAuth
from slack_bolt.oauth.oauth_settings import OAuthSettings
from teamiclink.slack.store_state import RedisOAuthStateStore
from teamiclink.app import create_app
from redis import Redis
import psycopg2.extras

psycopg2.extras.register_uuid()

config = AppConfig.load_from_env()

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
            )
        ),
    )
)
app = create_app(slack_handler=slack_handler)
