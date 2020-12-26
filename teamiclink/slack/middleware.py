from teamiclink.slack.store_install import TeamiclinkInstallStore
from typing import Callable, ClassVar
from slack_bolt.context import BoltContext
from slack_bolt.response import BoltResponse


class SlackMiddleware:
    INSTALL_STORE: ClassVar[TeamiclinkInstallStore]
    CLIENT_ID: ClassVar[str]
    CLIENT_SECRET: ClassVar[str]

    INSTALL_STORE_KEY: ClassVar[str] = "install_store"
    CLIENT_ID_KEY: ClassVar[str] = "client_id"
    CLIENT_SECRET_KEY: ClassVar[str] = "client_secret"

    @staticmethod
    def set_variable(
        install_store: TeamiclinkInstallStore, client_id: str, client_secret: str
    ):
        SlackMiddleware.INSTALL_STORE = install_store
        SlackMiddleware.CLIENT_ID = client_id
        SlackMiddleware.CLIENT_SECRET = client_secret

    @staticmethod
    def ctx_install_store(context: BoltContext, next: Callable[[], BoltResponse]):
        context[SlackMiddleware.INSTALL_STORE_KEY] = SlackMiddleware.INSTALL_STORE
        next()

    @staticmethod
    def ctx_client_id(context: BoltContext, next: Callable[[], BoltResponse]):
        context[SlackMiddleware.CLIENT_ID_KEY] = SlackMiddleware.CLIENT_ID
        next()

    @staticmethod
    def ctx_client_secret(context: BoltContext, next: Callable[[], BoltResponse]):
        context[SlackMiddleware.CLIENT_SECRET_KEY] = SlackMiddleware.CLIENT_SECRET
        next()
