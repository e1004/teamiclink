from flask.views import MethodView
from typing import ClassVar


class InstallController(MethodView):
    URI: ClassVar[str] = "/install"

    def get(self):
        return "Tere"
