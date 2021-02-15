from unittest.mock import MagicMock
from uuid import uuid4, UUID

from slack_bolt import Ack
from slack_bolt.context import BoltContext
from teamiclink.slack.actions import delete_goal
from teamiclink.slack.middleware import SlackMiddleware
from teamiclink.slack.store_goal import GoalStore


def test_it_deletes_goal():
    # given
    ack = MagicMock(spec=Ack)
    context = BoltContext()
    goal_store = MagicMock(spec=GoalStore)
    context[SlackMiddleware.GOAL_STORE_KEY] = goal_store
    context["team_id"] = "any_team_id"
    payload = dict(value=str(uuid4()))

    # when
    delete_goal(ack=ack, payload=payload, context=context)
    ack_calls = ack.call_args.kwargs

    # then
    assert ack_calls["response_type"] == "ephemeral"
    assert ack_calls["text"] is not None
    goal_store.delete_goal.assert_called_once_with(id=UUID(payload["value"]))
