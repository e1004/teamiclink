from dataclasses import dataclass
from upt.team.model import Team
from uuid import UUID


@dataclass
class TeamRepositiry:
    data_source_name: str

    def create_team(self, slack_team_id: str, access_token: str) -> Team:
        return Team(
            id=UUID("b11a530b-5acc-46b6-8125-e4812eb5047b"), slack_team_id=slack_team_id
        )
