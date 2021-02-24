import logging
from typing import Any, Dict, Type
from uuid import UUID

from slack_bolt import App, BoltContext, Ack
from teamiclink.slack.middleware import SlackMiddleware
from teamiclink.slack.store_goal import GoalStore
from slack_sdk import WebClient

LOG = logging.getLogger(__name__)


def delete_goal(
    context: BoltContext, payload: Dict[str, Any], ack: Ack, client: WebClient
):
    ack()
    goal_store: GoalStore = context[SlackMiddleware.GOAL_STORE_KEY]
    goal_store.delete_goal(id=UUID(payload["value"]))
    message = f"Deleted goal {payload['value']}"
    LOG.info(message)
    client.chat_postEphemeral(
        text=message, user=context["user_id"], channel=context["channel_id"]
    )


def register_actions(app: App, middleware: Type[SlackMiddleware]) -> None:
    action_delete_goal = app.action(
        constraints={"action_id": "delete_goal"}, middleware=[middleware.ctx_goal_store]
    )
    assert action_delete_goal
    action_delete_goal(delete_goal)
