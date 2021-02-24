from unittest.mock import ANY, MagicMock
from uuid import uuid4, UUID

from slack_bolt import Ack
from slack_bolt.context import BoltContext
from teamiclink.slack.actions import delete_goal
from teamiclink.slack.middleware import SlackMiddleware
from teamiclink.slack.store_goal import GoalStore
from slack_sdk import WebClient


def test_it_deletes_goal():
    # given
    ack = MagicMock(spec=Ack)
    context = BoltContext()
    goal_store = MagicMock(spec=GoalStore)
    context[SlackMiddleware.GOAL_STORE_KEY] = goal_store
    context["user_id"] = "any_user_id"
    context["channel_id"] = "any_channel_id"
    payload = dict(value=str(uuid4()))
    client = MagicMock(spec=WebClient)

    # when
    delete_goal(ack=ack, payload=payload, context=context, client=client)

    # then
    ack.assert_called_once()
    goal_store.delete_goal.assert_called_once_with(id=UUID(payload["value"]))
    client.chat_postEphemeral.assert_called_once_with(
        text=ANY, user=context["user_id"], channel=context["channel_id"]
    )
