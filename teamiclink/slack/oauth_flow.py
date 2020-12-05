from slack_bolt.oauth import OAuthFlow
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class TeamiclinkOAuth(OAuthFlow):
    def handle_installation(self, request: BoltRequest) -> BoltResponse:
        state = self.issue_new_state(request)
        url = self.build_authorize_url(state, request)
        set_cookie_value = self.settings.state_utils.build_set_cookie_for_new_state(
            state
        )
        return BoltResponse(
            status=302,
            headers={
                "Location": [url],
                "Set-Cookie": [set_cookie_value],
            },
        )
