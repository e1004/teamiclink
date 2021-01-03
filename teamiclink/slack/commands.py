import logging
from teamiclink.slack.view_goal_create import CREATE_GOAL
from teamiclink.slack.middleware import SlackMiddleware
from slack_bolt import Ack, App
from slack_sdk import WebClient
from slack_bolt.context import BoltContext
from typing import Any, Dict, Type

LOG = logging.getLogger(__name__)


def create_goal(ack: Ack, client: WebClient, body: Dict[str, Any]):
    ack()
    LOG.info("/create_goal")
    client.views_open(trigger_id=body["trigger_id"], view=CREATE_GOAL)


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

    cmd_create_goal = app.command(command="/t-goal")
    assert cmd_create_goal
    cmd_create_goal(create_goal)
