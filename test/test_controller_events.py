from contextlib import suppress
from test.conftest import Target
from unittest.mock import call

from flask import request
from teamiclink.slack.events import app_uninstalled


def test_it_calls_slack_handler(mocker, target: Target):
    # given
    handler = mocker.spy(target.slack_handler, "handle")

    # when
    with suppress(IndexError):
        target.client.post("/slack/events")

    # then
    handler.assert_called_once_with(req=request)


def test_it_registers_events(target: Target):
    # given
    slack_controller = target.client.application.view_functions["slack_events"]

    # when
    with suppress(Exception):
        slack_controller()
    calls = target.slack_handler.app.event.mock_calls

    # then
    assert calls[0] == call(
        event="app_uninstalled", middleware=[target.slack_middleware.ctx_install_store]
    )
    assert calls[1] == call()(app_uninstalled)
