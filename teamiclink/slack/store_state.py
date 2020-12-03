from typing import ClassVar, Optional
from slack_sdk.oauth import OAuthStateStore
from dataclasses import dataclass
from redis import Redis
import uuid


@dataclass
class RedisOAuthStateStore(OAuthStateStore):
    redis: Redis

    EXPIRY_SECONDS: ClassVar[int] = 300
    EMPTY_VALUE: ClassVar[str] = "."

    def issue(self, *args, **kwargs) -> str:
        state = str(uuid.uuid4())
        self.redis.set(name=state, value=self.EMPTY_VALUE, ex=self.EXPIRY_SECONDS)
        return state

    def consume(self, state: str) -> bool:
        value: Optional[bytes] = self.redis.get(name=state)
        if not value:
            return False
        decoded_value = value.decode("utf-8")
        if decoded_value == self.EMPTY_VALUE:
            self.redis.delete(state)
            return True
        return False
