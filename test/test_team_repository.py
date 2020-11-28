from test.conftest import DB_USER_REGULAR, DB_USER_ROOT

import pytest
from upt.database import Database
from upt.team.repository import TeamRepositiry


@pytest.mark.usefixtures("clean_db")
def test_it_creates_team():
    # given
    repository = TeamRepositiry(data_source_name=DB_USER_REGULAR)
    slack_team_id = "any_slack_team_id"
    access_token = "any_access_token"

    # when
    result = repository.create_team(
        slack_team_id=slack_team_id, access_token=access_token
    )
    with Database.connect(DB_USER_ROOT) as connection:
        with Database.create_cursor(connection) as cursor:
            cursor.execute(
                f"SELECT access_token FROM upt.team WHERE slack_team_id = '{slack_team_id}'"
            )
            db_response = cursor.fetchone()

    # then
    assert result.slack_team_id == slack_team_id
    assert result.id
    assert db_response["access_token"] == access_token
