from upt.install import InstallController
from unittest.mock import MagicMock
from slack_bolt.oauth import OAuthFlow
from flask import request


def test_it_redirects_to_install_url(target):
    # given
    state = "any_status"
    url = "https://any_url.com"
    oauth_flow = MagicMock(spec=OAuthFlow)
    oauth_flow.issue_new_state.return_value = state
    oauth_flow.build_authorize_url.return_value = url
    target.slack_handler.app.oauth_flow = oauth_flow

    # when
    result = target.client.get(InstallController.URI)

    # then
    assert result.status_code == 302
    oauth_flow.issue_new_state.assert_called_once_with(request=request)
    oauth_flow.build_authorize_url.assert_called_once_with(state=state, request=request)
