from upt.team.repository import TeamRepositiry


def test_it_creates_team():
    # given
    repository = TeamRepositiry(data_source_name="any_dsn")
    slack_team_id = "any_slack_team_id"
    access_token = "any_access_token"

    # when
    result = repository.create_team(
        slack_team_id=slack_team_id, access_token=access_token
    )

    # then
    assert result.slack_team_id == slack_team_id
    assert result.id
