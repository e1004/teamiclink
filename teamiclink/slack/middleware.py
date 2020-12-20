from teamiclink.slack.store_install import TeamiclinkInstallStore
from typing import Callable, ClassVar
from slack_bolt.context import BoltContext
from slack_bolt.response import BoltResponse
from teamiclink.slack.ctx_keys import INSTALL_STORE_CTX_KEYS


class SlackMiddleware:
    INSTALL_STORE: ClassVar[TeamiclinkInstallStore]

    @staticmethod
    def ctx_install_store(context: BoltContext, next: Callable[[], BoltResponse]):
        context[INSTALL_STORE_CTX_KEYS] = SlackMiddleware.INSTALL_STORE
        next()
