from teamiclink.slack.oauth_flow import TeamiclinkOAuth
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.request.request import BoltRequest


def test_it_redirects(mocker):
    # given
    oauth = TeamiclinkOAuth(
        settings=OAuthSettings(
            client_id="any_client_id", client_secret="any_client_secret"
        )
    )
    issue_state = mocker.patch.object(oauth, "issue_new_state")
    issue_state.return_value = "any_state"
    build_url = mocker.patch.object(oauth, "build_authorize_url")
    build_url.return_value = "https://any_url.com"
    build_cookie = mocker.patch.object(
        oauth.settings.state_utils, "build_set_cookie_for_new_state"
    )
    build_cookie.return_value = "any_cookie"
    bolt_request = BoltRequest(body="any_body")

    # when
    result = oauth.handle_installation(request=bolt_request)

    # then
    assert result.status == 302
    assert result.headers["location"] == [build_url.return_value]
    assert result.headers["set-cookie"] == [build_cookie.return_value]
    issue_state.assert_called_once_with(bolt_request)
    build_url.assert_called_once_with(issue_state.return_value, bolt_request)
    build_cookie.assert_called_once_with(issue_state.return_value)
