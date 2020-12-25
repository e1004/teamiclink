import logging
from typing import Any, Dict, Type

from slack_bolt.context import BoltContext
from teamiclink.slack.ctx_keys import INSTALL_STORE_CTX_KEYS
from teamiclink.slack.store_install import TeamiclinkInstallStore
from slack_bolt import App
from teamiclink.slack.middleware import SlackMiddleware

LOGGER = logging.getLogger(__name__)


def app_uninstalled(context: BoltContext, event: Dict[str, Any]):
    assert context.team_id
    install_store: TeamiclinkInstallStore = context[INSTALL_STORE_CTX_KEYS]
    LOGGER.info(f"uninstall: delete team id {context.team_id}, event {event}")
    install_store.delete_bot(team_id=context.team_id)


def register_events(app: App, middleware: Type[SlackMiddleware]):
    event_uninstall = app.event(
        event="app_uninstalled", middleware=[middleware.ctx_install_store]
    )
    assert event_uninstall
    event_uninstall(app_uninstalled)
