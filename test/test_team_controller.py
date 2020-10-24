from upt.team.controller import TeamController


def test_it_returns_tere(target):
    # given
    url = TeamController.URI

    # when
    result = target.client.get(url)

    # then
    assert result.status_code == 201
