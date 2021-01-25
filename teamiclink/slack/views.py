import logging
from teamiclink.slack.view_goal_create import (
    CREATE_GOAL_CALLBACK_ID,
    add_goal_to_payload,
)
from typing import Any, Dict, Type
from slack_bolt import Ack, App
from slack_bolt.context import BoltContext
from teamiclink.slack.middleware import SlackMiddleware

LOG = logging.getLogger(__name__)


@add_goal_to_payload
def create_goal(ack: Ack, payload: Dict[str, Any], context: BoltContext):
    ack()

    LOG.info("created new goal")


def register_views(app: App, middleware: Type[SlackMiddleware]) -> None:
    view_create_goal = app.view(constraints=CREATE_GOAL_CALLBACK_ID, middleware=[])
    assert view_create_goal
    view_create_goal(create_goal)
