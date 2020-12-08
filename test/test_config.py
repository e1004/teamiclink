from teamiclink.config import AppConfig
import json


def test_it_loads_from_environment(monkeypatch):
    # given
    dsn = "any_dsn"
    monkeypatch.setenv("DSN", dsn)
    path_logging_config = "any_logging_config_path"
    monkeypatch.setenv("PATH_LOGGING_CONFIG", path_logging_config)
    slack_client_id = "any_slack_client_id"
    monkeypatch.setenv("SLACK_CLIENT_ID", slack_client_id)
    slack_client_secret = "any_slack_client_secret"
    monkeypatch.setenv("SLACK_CLIENT_SECRET", slack_client_secret)
    slack_signing_secret = "any_slack_client_secret"
    monkeypatch.setenv("SLACK_SIGNING_SECRET", slack_signing_secret)
    slack_permissions = ["app_mentions:read", "channels:history"]
    monkeypatch.setenv("SLACK_PERMISSIONS", json.dumps(slack_permissions))
    redis_db_install_state = 5
    monkeypatch.setenv("REDIS_DB_INSTALL_STATE", str(redis_db_install_state))
    redis_host = "any_redis_host"
    monkeypatch.setenv("REDIS_HOST", redis_host)
    redis_port = 6943
    monkeypatch.setenv("REDIS_PORT", str(redis_port))
    redis_password = "any_redis_password"
    monkeypatch.setenv("REDIS_PASSWORD", redis_password)
    redis_socket_timeout_seconds = 3.0
    monkeypatch.setenv(
        "REDIS_SOCKET_TIMEOUT_SECONDS", str(int(redis_socket_timeout_seconds))
    )
    redis_socket_connect_timeout_seconds = 10.0
    monkeypatch.setenv(
        "REDIS_SOCKET_CONNECT_TIMEOUT_SECONDS",
        str(int(redis_socket_connect_timeout_seconds)),
    )

    # when
    result = AppConfig.load_from_env()

    # then
    assert result.dsn == dsn
    assert result.slack_client_id == slack_client_id
    assert result.slack_client_secret == slack_client_secret
    assert result.slack_signing_secret == slack_signing_secret
    assert result.slack_permissions == slack_permissions
    assert result.redis_db_install_state == redis_db_install_state
    assert result.redis_host == redis_host
    assert result.redis_port == redis_port
    assert result.redis_password == redis_password
    assert result.redis_socket_timeout_seconds == redis_socket_timeout_seconds
    assert (
        result.redis_socket_connect_timeout_seconds
        == redis_socket_connect_timeout_seconds
    )
