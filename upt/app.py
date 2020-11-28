from flask import request
import psycopg2.extras
from flask import Flask
from slack_bolt.adapter.flask import SlackRequestHandler


psycopg2.extras.register_uuid()


def create_app(slack_handler: SlackRequestHandler):
    app = Flask(__name__)

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
    return app
