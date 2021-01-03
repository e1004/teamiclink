from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler


def register_url_rules(slack_handler: SlackRequestHandler, app: Flask):
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

    app.add_url_rule(
        rule="/slack/interactions",
        endpoint="slack_interactions",
        view_func=forward_slack,
        methods=["POST"],
    )
