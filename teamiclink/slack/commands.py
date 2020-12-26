import logging
from teamiclink.slack.middleware import SlackMiddleware
from slack_bolt import Ack
from slack_sdk import WebClient
from slack_bolt.context import BoltContext

LOG = logging.getLogger(__name__)


def uninstall(ack: Ack, client: WebClient, context: BoltContext):
    ack()
    LOG.info("/uninstalling")
    client.apps_uninstall(
        client_id=context[SlackMiddleware.CLIENT_ID_KEY],
        client_secret=context[SlackMiddleware.CLIENT_SECRET_KEY],
    )
