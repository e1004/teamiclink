import psycopg2.extras
from flask import Flask
from slack_bolt.adapter.flask import SlackRequestHandler

from upt.install import InstallController, OAuthRedirectController


psycopg2.extras.register_uuid()


def create_app(slack_handler: SlackRequestHandler):
    app = Flask(__name__)
    app.add_url_rule(
        OAuthRedirectController.URI,
        view_func=OAuthRedirectController.as_view("oauth_redirect_controller", slack_handler=slack_handler),
    )
    app.add_url_rule(
        InstallController.URI,
        view_func=InstallController.as_view(
            "install_controller", slack_handler=slack_handler
        ),
    )
    return app
