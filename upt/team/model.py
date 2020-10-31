from dataclasses import dataclass
from uuid import UUID


@dataclass
class Team:
    id: UUID
    slack_team_id: str
