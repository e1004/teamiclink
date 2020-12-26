from teamiclink.slack.middleware import SlackMiddleware
from typing import Dict
from unittest.mock import MagicMock

from slack_bolt.context import BoltContext
from teamiclink.slack.events import app_uninstalled
from teamiclink.slack.store_install import TeamiclinkInstallStore


def test_app_uninstalled_deletes_bot():
    # given
    context = BoltContext()
    install_store = MagicMock(spec=TeamiclinkInstallStore)
    context[SlackMiddleware.INSTALL_STORE_KEY] = install_store
    context["team_id"] = "any_tema_id"

    # when
    app_uninstalled(context=context, event=Dict)

    # then
    install_store.delete_bot.assert_called_once_with(team_id=context["team_id"])
