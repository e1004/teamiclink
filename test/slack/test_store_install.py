from test.conftest import DB_USER_REGULAR

import pytest
from teamiclink.slack.store_install import TeamiclinkInstallStore
from datetime import datetime, timezone


@pytest.mark.usefixtures("clean_db")
def test_it_creates_slack_bot():
    # given
    install_store = TeamiclinkInstallStore(data_source_name=DB_USER_REGULAR)
    team_id = "any_slack_team_id"
    bot_token = "any_bot_token"
    bot_id = "any_bot_id"
    bot_user_id = "any_bot_user_id"
    installed_at = datetime.now(timezone.utc)

    # when
    result = install_store.create_bot(
        team_id=team_id,
        bot_token=bot_token,
        bot_id=bot_id,
        bot_user_id=bot_user_id,
        installed_at=installed_at,
    )
    # then
    assert result.team_id == team_id
    assert result.id is not None
    assert result.bot_id == bot_id
    assert result.bot_user_id == bot_user_id
    assert result.installed_at == installed_at
