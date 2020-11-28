from flask import request
from test.conftest import Target
import pytest


@pytest.mark.parametrize("uri", ["/slack/install", "/slack/oauth_redirect"])
def test_it_calls_slack_handler(uri, mocker, target: Target):
    # given
    handler = mocker.spy(target.slack_handler, "handle")

    # when
    target.client.get(uri)

    # then
    handler.assert_called_once_with(req=request)
