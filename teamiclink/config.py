from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import List


@dataclass
class AppConfig:
    dsn: str
    path_logging_config: str
    slack_client_id: str
    slack_client_secret: str
    slack_signing_secret: str
    slack_permissions: List[str]
    redis_db_install_state: int
    redis_host: str
    redis_port: int
    redis_password: str
    redis_socket_timeout_seconds: float
    redis_socket_connect_timeout_seconds: float

    @staticmethod
    def load_from_env() -> AppConfig:
        return AppConfig(
            dsn=os.environ["DSN"],
            path_logging_config=os.environ["PATH_LOGGING_CONFIG"],
            slack_client_id=os.environ["SLACK_CLIENT_ID"],
            slack_client_secret=os.environ["SLACK_CLIENT_SECRET"],
            slack_signing_secret=os.environ["SLACK_SIGNING_SECRET"],
            slack_permissions=json.loads(os.environ["SLACK_PERMISSIONS"]),
            redis_db_install_state=int(os.environ["REDIS_DB_INSTALL_STATE"]),
            redis_host=os.environ["REDIS_HOST"],
            redis_port=int(os.environ["REDIS_PORT"]),
            redis_password=os.environ["REDIS_PASSWORD"],
            redis_socket_timeout_seconds=float(
                os.environ["REDIS_SOCKET_TIMEOUT_SECONDS"]
            ),
            redis_socket_connect_timeout_seconds=float(
                os.environ["REDIS_SOCKET_CONNECT_TIMEOUT_SECONDS"]
            ),
        )
