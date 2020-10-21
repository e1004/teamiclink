from dataclasses import dataclass
from typing import ClassVar

from flask import redirect
from flask.views import MethodView
from upt.config import AppConfig


@dataclass
class InstallController(MethodView):
    config: AppConfig

    URI: ClassVar[str] = "/install"
    SLACK_AUTH_URI: ClassVar[str] = "https://slack.com/oauth/v2/authorize"

    def get(self):
        return redirect(
            location=(
                f"{self.SLACK_AUTH_URI}?"
                f"client_id={self.config.slack_client_id}"
                f"scope={','.join(self.config.slack_permissions)}"
            )
        )
