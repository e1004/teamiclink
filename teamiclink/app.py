from teamiclink.slack.middleware import SlackMiddleware
from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

from teamiclink.slack.events import app_uninstalled
from typing import Type


def create_app(
    slack_handler: SlackRequestHandler, slack_middleware: Type[SlackMiddleware]
) -> Flask:
    app = Flask("teamiclink")

    slack_handler.app.event(  # type: ignore
        event="app_uninstalled", middleware=[slack_middleware.ctx_install_store]
    )(app_uninstalled)

    def forward_slack():
        return slack_handler.handle(req=request)

    app.add_url_rule(
        rule="/slack/install",
        endpoint="slack_install",
        view_func=forward_slack,
        methods=["GET"],
    )
    app.add_url_rule(
        rule="/slack/oauth_redirect",
        endpoint="slack_oauth_redirect",
        view_func=forward_slack,
        methods=["GET"],
    )

    app.add_url_rule(
        rule="/slack/events",
        endpoint="slack_events",
        view_func=forward_slack,
        methods=["POST"],
    )
    return app
