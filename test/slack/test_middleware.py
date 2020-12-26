from test.conftest import Target
from unittest.mock import MagicMock

from slack_bolt.context import BoltContext
from teamiclink.slack.middleware import SlackMiddleware


def test_it_adds_install_store_to_ctx_and_calls_next(target: Target):
    # given
    context = BoltContext()
    next_func = MagicMock()

    # when
    target.slack_middleware.ctx_install_store(context=context, next=next_func)

    # then
    assert (
        context[SlackMiddleware.INSTALL_STORE_KEY]
        == target.slack_middleware.INSTALL_STORE
    )
    next_func.assert_called_once_with()


def test_it_adds_client_id_to_ctx_and_calls_next(target: Target):
    # given
    context = BoltContext()
    next_func = MagicMock()

    # when
    target.slack_middleware.ctx_client_id(context=context, next=next_func)

    # then
    assert context[SlackMiddleware.CLIENT_ID_KEY] == target.slack_middleware.CLIENT_ID
    next_func.assert_called_once_with()


def test_it_adds_client_secret_to_ctx_and_calls_next(target: Target):
    # given
    context = BoltContext()
    next_func = MagicMock()

    # when
    target.slack_middleware.ctx_client_secret(context=context, next=next_func)

    # then
    assert (
        context[SlackMiddleware.CLIENT_SECRET_KEY]
        == target.slack_middleware.CLIENT_SECRET
    )
    next_func.assert_called_once_with()
