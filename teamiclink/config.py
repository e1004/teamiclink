from typing import List

from dataclasses import dataclass


@dataclass
class AppConfig:
    slack_client_id: str
    slack_permissions: List[str]
