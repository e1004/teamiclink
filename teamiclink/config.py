from __future__ import annotations

from typing import List
from pydantic import BaseSettings


class AppConfig(BaseSettings):
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
