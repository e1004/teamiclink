import pytest
from teamiclink.slack.store_goal import GoalStore
from test.conftest import DB_USER_REGULAR
from teamiclink.slack.store_install import TeamiclinkInstallStore
from datetime import datetime

TEAM_ID1, TEAM_ID2 = "any_team_id1", "any_team_id2"


@pytest.fixture
def slack_bot():
    store_install = TeamiclinkInstallStore(data_source_name=DB_USER_REGULAR)
    store_install.create_bot(
        team_id=TEAM_ID2,
        bot_id="any_bot_id",
        bot_token="any_bot_token",
        bot_user_id="any_bot_user_id",
        installed_at=datetime.today(),
    )
    yield store_install.create_bot(
        team_id=TEAM_ID1,
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
    result = goal_store.create_goal(content=content, slack_team_id=TEAM_ID1)

    # then
    assert result.content == content
    assert result.slack_team_id == TEAM_ID1


@pytest.mark.usefixtures("clean_db", "slack_bot")
def test_it_reads_goals(goal_store: GoalStore):
    # given
    goal1 = goal_store.create_goal(content="bb", slack_team_id=TEAM_ID1)
    goal2 = goal_store.create_goal(content="aa", slack_team_id=TEAM_ID1)
    goal_store.create_goal(content="cc", slack_team_id=TEAM_ID2)

    # when
    result = goal_store.read_goals(slack_team_id=TEAM_ID1)

    # then
    assert len(result) == 2
    assert result[1].content == goal1.content
    assert result[0].content == goal2.content
    assert result[0].slack_team_id == result[1].slack_team_id == TEAM_ID1
