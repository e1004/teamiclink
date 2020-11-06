from dataclasses import dataclass
from upt.team.model import Team
from upt.database import Database


@dataclass
class TeamRepositiry:
    data_source_name: str

    def create_team(self, slack_team_id: str, access_token: str) -> Team:
        query = """
            INSERT INTO upt.team(slack_team_id, access_token)
            VALUES (%(slack_team_id)s, %(access_token)s)
            RETURNING id, slack_team_id;
        """
        query_params = dict(slack_team_id=slack_team_id, access_token=access_token)
        with Database.connect(data_source_name=self.data_source_name) as connection:
            with Database.create_cursor(connection=connection) as cursor:
                cursor.execute(query, query_params)
                response = cursor.fetchone()

        return Team(**response)
