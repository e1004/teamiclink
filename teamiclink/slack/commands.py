import logging
from teamiclink.slack.middleware import SlackMiddleware
from slack_bolt import Ack, App
from slack_sdk import WebClient
from slack_bolt.context import BoltContext
from typing import Type

LOG = logging.getLogger(__name__)


def uninstall(ack: Ack, client: WebClient, context: BoltContext):
    ack()
    LOG.info("/uninstalling")
    client.apps_uninstall(
        client_id=context[SlackMiddleware.CLIENT_ID_KEY],
        client_secret=context[SlackMiddleware.CLIENT_SECRET_KEY],
    )


def register_commands(app: App, middleware: Type[SlackMiddleware]):
    cmd_uninstall = app.command(
        command="/teamiclink-uninstall",
        middleware=[middleware.ctx_client_secret, middleware.ctx_client_id],
    )
    assert cmd_uninstall
    cmd_uninstall(uninstall)
