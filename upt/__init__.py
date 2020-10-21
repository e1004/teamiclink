from flask import Flask
from upt.install.controller import InstallController


def create_app():
    app = Flask(__name__)
    app.add_url_rule(
        InstallController.URI, view_func=InstallController.as_view("install_controller")
    )
    return app


app = create_app()
