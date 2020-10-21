from dataclasses import dataclass


@dataclass
class AppConfig:
    slack_client_id: str
    slack_permissions: list[str]
