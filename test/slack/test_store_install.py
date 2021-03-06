from datetime import datetime, timezone
from test.conftest import DB_USER_REGULAR
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from freezegun import freeze_time
from slack_sdk.oauth.installation_store import Installation
from teamiclink.slack.errors import MissingBotError
from teamiclink.slack.model import TeamiclinkBot
from teamiclink.slack.store_install import TeamiclinkInstallStore

TEAM_ID, BOT_TOKEN, BOT_ID, BOT_USER_ID = (
    str(uuid4()),
    str(uuid4()),
    str(uuid4()),
    str(uuid4()),
)
INSTALLED_AT = datetime(2010, 11, 25, 8, 45, 14, 357581, tzinfo=timezone.utc)


@pytest.fixture
def install_store():
    yield TeamiclinkInstallStore(data_source_name=DB_USER_REGULAR)


@pytest.fixture
def slack_bot(install_store: TeamiclinkInstallStore):
    yield install_store.create_bot(
        team_id=TEAM_ID,
        bot_token=BOT_TOKEN,
        bot_id=BOT_ID,
        bot_user_id=BOT_USER_ID,
        installed_at=INSTALLED_AT,
    )


@pytest.mark.usefixtures("clean_db")
def test_it_creates_slack_bot(install_store: TeamiclinkInstallStore):
    # when
    result = install_store.create_bot(
        team_id=TEAM_ID,
        bot_token=BOT_TOKEN,
        bot_id=BOT_ID,
        bot_user_id=BOT_USER_ID,
        installed_at=INSTALLED_AT,
    )
    # then
    assert result.team_id == TEAM_ID
    assert result.id is not None
    assert result.bot_id == BOT_ID
    assert result.bot_user_id == BOT_USER_ID
    assert result.installed_at == INSTALLED_AT
    assert result.bot_token == BOT_TOKEN


@pytest.mark.usefixtures("clean_db")
def test_it_reads_slack_bot(
    install_store: TeamiclinkInstallStore, slack_bot: TeamiclinkBot
):
    # when
    result = install_store.read_bot(team_id=slack_bot.team_id)

    # then
    assert result.team_id == slack_bot.team_id
    assert result.bot_id == slack_bot.bot_id
    assert result.bot_user_id == slack_bot.bot_user_id
    assert result.installed_at == slack_bot.installed_at
    assert result.bot_token == slack_bot.bot_token


def test_it_finds_installation(install_store: TeamiclinkInstallStore, mocker):
    # given
    read = mocker.patch.object(install_store, "read_bot")
    bot = TeamiclinkBot(
        id=uuid4(),
        team_id=TEAM_ID,
        bot_token=BOT_TOKEN,
        bot_id=BOT_ID,
        bot_user_id=BOT_USER_ID,
        installed_at=INSTALLED_AT,
    )
    read.return_value = bot

    # when
    result = install_store.find_installation(team_id=bot.team_id)

    # then
    read.assert_called_once_with(team_id=TEAM_ID)
    assert result.user_id == ""
    assert result.team_id == bot.team_id
    assert result.bot_id == bot.bot_id
    assert result.bot_user_id == bot.bot_user_id
    assert result.bot_token == bot.bot_token
    assert result.installed_at == bot.installed_at.timestamp()


def test_it_returns_none_when_finding_missing_bot(
    install_store: TeamiclinkInstallStore, mocker
):
    # given
    read = mocker.patch.object(install_store, "read_bot")
    read.side_effect = MissingBotError("any_message")

    # when
    result = install_store.find_installation(team_id=TEAM_ID)

    # then
    assert result is None


@pytest.mark.usefixtures("clean_db")
def test_it_raises_error_when_reading_missing_bot(
    install_store: TeamiclinkInstallStore,
):
    # when
    try:
        install_store.read_bot(team_id=TEAM_ID)
        pytest.fail("expected error")

    # then
    except MissingBotError as error:
        assert TEAM_ID in str(error)


@pytest.mark.usefixtures("clean_db")
def test_it_deletes_bot(
    install_store: TeamiclinkInstallStore, slack_bot: TeamiclinkBot
):
    # when
    result = install_store.delete_bot(team_id=slack_bot.team_id)

    # then
    assert result == 1


@pytest.mark.usefixtures("clean_db")
def test_it_updates_bot(
    install_store: TeamiclinkInstallStore, slack_bot: TeamiclinkBot
):
    # given
    new_bot_id = "any_new_bot_id"
    new_bot_token = "any_new_bot_token"
    new_bot_user_id = "any_new_bot_user_id"

    # when
    result = install_store.update_bot(
        team_id=slack_bot.team_id,
        bot_id=new_bot_id,
        bot_token=new_bot_token,
        bot_user_id=new_bot_user_id,
    )

    # then
    assert result.team_id == slack_bot.team_id
    assert result.bot_id == new_bot_id
    assert result.bot_token == new_bot_token
    assert result.bot_user_id == new_bot_user_id


@pytest.mark.usefixtures("clean_db")
def test_it_updates_fields_when_creating_existing_bot(
    install_store: TeamiclinkInstallStore, slack_bot: TeamiclinkBot, mocker
):
    # given
    updater = mocker.patch.object(install_store, "update_bot")
    updater.return_value = slack_bot

    # when
    result = install_store.create_bot(
        team_id=slack_bot.team_id,
        bot_token=slack_bot.bot_token,
        bot_id=slack_bot.bot_id,
        bot_user_id=slack_bot.bot_user_id,
        installed_at=slack_bot.installed_at,
    )

    # then
    assert result == updater.return_value
    updater.assert_called_once_with(
        team_id=slack_bot.team_id,
        bot_token=slack_bot.bot_token,
        bot_id=slack_bot.bot_id,
        bot_user_id=slack_bot.bot_user_id,
    )


@freeze_time("2017-09-23 13:12:34")
def test_it_calls_create_when_saving(install_store: TeamiclinkInstallStore, mocker):
    # given
    create = mocker.patch.object(install_store, "create_bot")
    installation = MagicMock(spec=Installation)
    installation.team_id = "any_team_id"
    installation.bot_token = "any_access_token"
    installation.bot_id = "any_bot_id"
    installation.bot_user_id = "any_bot_user_id"

    # when
    install_store.save(installation=installation)

    # then
    create.assert_called_once_with(
        team_id=installation.team_id,
        bot_token=installation.bot_token,
        bot_id=installation.bot_id,
        bot_user_id=installation.bot_user_id,
        installed_at=datetime(2017, 9, 23, 13, 12, 34, tzinfo=timezone.utc),
    )
