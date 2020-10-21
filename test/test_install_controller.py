from upt.install.controller import InstallController


def test_it_returns_tere(target):
    # given
    url = InstallController.URI

    # when
    result = target.client.get(url)

    # then
    assert result.status_code == 302
    assert result.location == (
        f"{InstallController.SLACK_AUTH_URI}?"
        f"client_id={target.config.slack_client_id}"
        f"scope={','.join(target.config.slack_permissions)}"
    )
