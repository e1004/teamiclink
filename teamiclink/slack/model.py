from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class TeamiclinkBot:
    id: UUID
    team_id: str
    bot_token: str
    bot_id: str
    bot_user_id: str
    installed_at: datetime
