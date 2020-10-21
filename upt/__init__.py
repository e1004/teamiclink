from flask import Flask

from upt.config import AppConfig
from upt.install.controller import InstallController


def create_app(config: AppConfig):
    app = Flask(__name__)
    app.add_url_rule(
        InstallController.URI,
        view_func=InstallController.as_view("install_controller", config=config),
    )
    return app


config = AppConfig(slack_client_id="any_string", slack_permissions=[])
app = create_app(config=config)
