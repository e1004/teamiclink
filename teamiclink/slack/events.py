import logging
from typing import Any, Dict

from slack_bolt.context import BoltContext
from teamiclink.slack.ctx_keys import INSTALL_STORE_CTX_KEYS
from teamiclink.slack.store_install import TeamiclinkInstallStore

LOGGER = logging.getLogger(__name__)


def app_uninstalled(context: BoltContext, event: Dict[str, Any]):
    assert context.team_id
    install_store: TeamiclinkInstallStore = context[INSTALL_STORE_CTX_KEYS]
    LOGGER.info(f"uninstall: delete team id {context.team_id}, event {event}")
    install_store.delete_bot(team_id=context.team_id)
