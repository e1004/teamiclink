from upt.install.controller import InstallController


def test_it_returns_tere(target):
    # given
    url = InstallController.URI

    # when
    result = target.get(url)

    # then
    assert result.status_code == 200
    assert result.data.decode() == "Tere"
