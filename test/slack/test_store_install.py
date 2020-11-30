from teamiclink.slack.model import TeamiclinkBot
from uuid import uuid4
from test.conftest import DB_USER_REGULAR

import pytest
from teamiclink.slack.store_install import TeamiclinkInstallStore
from datetime import datetime, timezone

pytestmark = pytest.mark.usefixtures("clean_db")

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
