from unittest.mock import MagicMock
from slack_bolt.context import BoltContext
from teamiclink.slack.middleware import SlackMiddleware
from teamiclink.slack.commands import uninstall
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
