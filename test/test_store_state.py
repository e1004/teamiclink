from unittest.mock import MagicMock
from teamiclink.slack.store_state import uuid as state_store_uuid
import pytest
from redis import Redis
from teamiclink.slack.store_state import RedisOAuthStateStore


@pytest.fixture
def state_store():
    yield RedisOAuthStateStore(redis=MagicMock(spec=Redis))


def test_it_issues_state(state_store: RedisOAuthStateStore, mocker):
    # given
    uuid_generator = mocker.patch.object(state_store_uuid, "uuid4")
    uuid_generator.return_value = 16

    # when
    result = state_store.issue()

    # then
    assert result == str(uuid_generator.return_value)
    state_store.redis.set.assert_called_once_with(
        name=str(uuid_generator.return_value),
        value=state_store.EMPTY_VALUE,
        ex=state_store.EXPIRY_SECONDS,
    )


def test_it_consumes_state(state_store: RedisOAuthStateStore):
    # given
    state = "any_value"
    state_store.redis.get.return_value = b"."

    # when
    result = state_store.consume(state=state)

    # then
    assert result is True
    state_store.redis.get.assert_called_once_with(name=state)
    state_store.redis.delete.assert_called_once_with(state)


@pytest.mark.parametrize("state_from_redis", [None, b"any_value"])
def test_it_returns_false_for_unwanted_state(
    state_from_redis, state_store: RedisOAuthStateStore
):
    # given
    state = "any_value"
    state_store.redis.get.return_value = state_from_redis

    # when
    result = state_store.consume(state=state)

    # then
    state_store.redis.delete.assert_not_called()
    assert result is False
