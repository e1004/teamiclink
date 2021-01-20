from unittest.mock import MagicMock

import pytest
from pydantic.errors import AnyStrMaxLengthError, AnyStrMinLengthError
from slack_bolt import Ack
from slack_bolt.context import BoltContext
from teamiclink.slack.model import GoalStr
from teamiclink.slack.view_goal_create import CREATE_GOAL_INPUT, CREATE_GOAL_INPUT_BLOCK
from teamiclink.slack.views import create_goal


def test_goal_creation_saves_goal_without_spaces():
    # given
    ack = MagicMock(spec=Ack)
    goal_content = "any_goal_content"
    payload = {
        "state": {
            "values": {
                CREATE_GOAL_INPUT_BLOCK: {CREATE_GOAL_INPUT: {"value": goal_content}}
            }
        }
    }
    context = BoltContext()

    # when
    create_goal(ack=ack, payload=payload, context=context)

    # then
    ack.assert_called_once()


@pytest.mark.parametrize(
    "goal_content, goal_error",
    [
        (
            " i ",
            AnyStrMinLengthError.msg_template.format(limit_value=GoalStr.min_length),
        ),
        (
            "i" * (GoalStr.max_length + 1),
            AnyStrMaxLengthError.msg_template.format(limit_value=GoalStr.max_length),
        ),
    ],
)
def test_goal_creation_returns_errors_for_invalid_goal(goal_content, goal_error):
    # given
    ack = MagicMock(spec=Ack)
    payload = {
        "state": {
            "values": {
                CREATE_GOAL_INPUT_BLOCK: {CREATE_GOAL_INPUT: {"value": goal_content}}
            }
        }
    }
    context = BoltContext()

    # when
    create_goal(ack=ack, payload=payload, context=context)
    ack_calls = ack.call_args.kwargs

    # then
    assert ack_calls["response_action"] == "errors"
    assert ack_calls["errors"] == {CREATE_GOAL_INPUT_BLOCK: goal_error}
