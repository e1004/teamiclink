from teamiclink.slack.view_goal_create import CREATE_GOAL
from unittest.mock import MagicMock
from slack_bolt.context import BoltContext
from teamiclink.slack.middleware import SlackMiddleware
from teamiclink.slack.commands import create_goal, uninstall
from slack_sdk import WebClient
from slack_bolt import Ack


def test_it_calls_uninstall_with_client_variables():
    # given
    ack = MagicMock(spec=Ack)
    client = MagicMock(spec=WebClient)
    context = BoltContext()
    context[SlackMiddleware.CLIENT_ID_KEY] = "any_client_id"
    context[SlackMiddleware.CLIENT_SECRET_KEY] = "any_client_secret"

    # when
    uninstall(ack=ack, client=client, context=context)

    # then
    ack.assert_called_once()
    client.apps_uninstall.assert_called_once_with(
        client_id=context[SlackMiddleware.CLIENT_ID_KEY],
        client_secret=context[SlackMiddleware.CLIENT_SECRET_KEY],
    )


def test_create_goal_opens_view():
    # given
    ack = MagicMock(spec=Ack)
    body = dict(trigger_id="any_trigger_id")
    client = MagicMock(spec=WebClient)

    # when
    create_goal(ack=ack, client=client, body=body)

    # then
    ack.assert_called_once()
    client.views_open.assert_called_once_with(
        trigger_id=body["trigger_id"], view=CREATE_GOAL
    )
