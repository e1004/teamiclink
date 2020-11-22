import psycopg2.extras
from flask import Flask
from slack_bolt.adapter.flask import SlackRequestHandler

from upt.install.controller import InstallController
from upt.team.controller import TeamController

psycopg2.extras.register_uuid()


def create_app(slack_handler: SlackRequestHandler):
    app = Flask(__name__)
    app.add_url_rule(
        TeamController.URI,
        view_func=TeamController.as_view("team_controller"),
    )
    app.add_url_rule(
        InstallController.URI,
        view_func=InstallController.as_view(
            "install_controller", slack_handler=slack_handler
        ),
    )
    return app
