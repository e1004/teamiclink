from dataclasses import dataclass
from typing import ClassVar

from flask import redirect, request
from flask.views import MethodView
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt.oauth import OAuthFlow


@dataclass
class InstallController(MethodView):
    slack_handler: SlackRequestHandler

    URI: ClassVar[str] = "/slack/install"

    def get(self):
        oauth_flow: OAuthFlow = self.slack_handler.app.oauth_flow
        state = oauth_flow.issue_new_state(request=request)
        url = oauth_flow.build_authorize_url(state=state, request=request)
        return redirect(location=url)


@dataclass
class OAuthRedirectController(MethodView):
    slack_handler: SlackRequestHandler

    URI: ClassVar[str] = "/slack/oath_redirect"

    def get(self):
        return self.slack_handler.handle(req=request)
