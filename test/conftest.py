from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock

import pytest
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt.app import App
from upt import create_app


@dataclass
class Target:
    client: Any
    slack_handler: SlackRequestHandler


@pytest.fixture
def target():
    slask_app = MagicMock(spec=App)
    slack_handler = SlackRequestHandler(app=slask_app)
    app = create_app(slack_handler=slack_handler)
    app.testing = True
    with app.test_client() as client:
        yield Target(client=client, slack_handler=slack_handler)
