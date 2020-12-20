from flask import request
from test.conftest import Target
from contextlib import suppress


def test_it_calls_slack_handler(mocker, target: Target):
    # given
    handler = mocker.spy(target.slack_handler, "handle")

    # when
    with suppress(IndexError):
        target.client.post("/slack/events")

    # then
    handler.assert_called_once_with(req=request)
