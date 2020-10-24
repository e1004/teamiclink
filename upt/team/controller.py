from dataclasses import dataclass
from typing import ClassVar

from flask.views import MethodView


@dataclass
class TeamController(MethodView):
    URI: ClassVar[str] = "/teams"

    def get(self):
        return "Tere", 201
