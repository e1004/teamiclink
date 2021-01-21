import pytest
from teamiclink.slack.store_goal import GoalStore
from test.conftest import DB_USER_REGULAR
from teamiclink.slack.store_install import TeamiclinkInstallStore
from datetime import datetime

TEAM_ID = "any_team_id"


@pytest.fixture
def slack_bot():
    store_install = TeamiclinkInstallStore(data_source_name=DB_USER_REGULAR)
    yield store_install.create_bot(
        team_id=TEAM_ID,
        bot_id="any_bot_id",
        bot_token="any_bot_token",
        bot_user_id="any_bot_user_id",
        installed_at=datetime.today(),
    )


@pytest.fixture
def goal_store():
    yield GoalStore(data_source_name=DB_USER_REGULAR)


@pytest.mark.usefixtures("clean_db", "slack_bot")
def test_it_creates_goal(goal_store: GoalStore):
    # given
    content = "any_content"

    # when
    result = goal_store.create_goal(content=content, slack_team_id=TEAM_ID)

    # then
    assert result.content == content
    assert result.slack_team_id == TEAM_ID
