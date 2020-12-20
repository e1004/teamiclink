from unittest.mock import MagicMock

from slack_bolt.context import BoltContext
from teamiclink.slack.ctx_keys import INSTALL_STORE_CTX_KEYS
from teamiclink.slack.middleware import SlackMiddleware
from teamiclink.slack.store_install import TeamiclinkInstallStore


def test_it_adds_install_store_to_ctx_and_calls_next():
    # given
    context = BoltContext()
    next_func = MagicMock()
    install_store = TeamiclinkInstallStore(data_source_name="any_dsn")
    SlackMiddleware.INSTALL_STORE = install_store

    # when
    SlackMiddleware.ctx_install_store(context=context, next=next_func)

    # then
    assert context[INSTALL_STORE_CTX_KEYS] == install_store
    next_func.assert_called_once_with()
