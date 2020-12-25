from contextlib import suppress
from test.conftest import Target

import pytest
from flask import request


def test_it_forwards_events_to_slack_handler(mocker, target: Target):
    # given
    handler = mocker.spy(target.slack_handler, "handle")

    # when
    with suppress(IndexError):
        target.client.post("/slack/events")

    # then
    handler.assert_called_once_with(req=request)


@pytest.mark.parametrize("uri", ["/slack/install", "/slack/oauth_redirect"])
def test_it_forwaerds_installation_to_slack_handler(uri, mocker, target: Target):
    # given
    handler = mocker.spy(target.slack_handler, "handle")

    # when
    target.client.get(uri)

    # then
    handler.assert_called_once_with(req=request)
