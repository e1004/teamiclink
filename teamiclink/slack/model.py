from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConstrainedStr


@dataclass
class TeamiclinkBot:
    id: UUID
    team_id: str
    bot_token: str
    bot_id: str
    bot_user_id: str
    installed_at: datetime


class GoalStr(ConstrainedStr):
    min_length = 2
    max_length = 420
    strip_whitespace = True


class GoalContent(BaseModel):
    content: GoalStr


class Goal(GoalContent):
    slack_team_id: str
