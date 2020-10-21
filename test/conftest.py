from upt import create_app
import pytest
from upt.config import AppConfig
from dataclasses import dataclass
from typing import Any


@dataclass
class Target:
    client: Any
    config: AppConfig


@pytest.fixture
def target():
    config = AppConfig(
        slack_client_id="any_slack_client_id", slack_permissions=["1:a", "2:a"]
    )
    app = create_app(config=config)
    app.testing = True
    with app.test_client() as client:
        return Target(client=client, config=config)
