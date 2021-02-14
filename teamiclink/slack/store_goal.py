from dataclasses import dataclass
from typing import List
from teamiclink.slack.model import Goal
from teamiclink.database import Database


@dataclass
class GoalStore:
    data_source_name: str

    def create_goal(self, content: str, slack_team_id: str) -> Goal:
        query = """
            INSERT INTO teamiclink.goal
            (slack_team_id, content)
            VALUES
            (%(slack_team_id)s, %(content)s)
            RETURNING slack_team_id, content, id;
        """
        query_params = dict(
            slack_team_id=slack_team_id,
            content=content,
        )
        with Database.connect(data_source_name=self.data_source_name) as connection:
            with Database.create_cursor(connection=connection) as cursor:
                cursor.execute(query, query_params)
                response = cursor.fetchone()

        return Goal(**response)

    def read_goals(self, slack_team_id: str) -> List[Goal]:
        query = """
            SELECT slack_team_id, content, id
            FROM teamiclink.goal
            WHERE slack_team_id = %(slack_team_id)s
            ORDER BY content ASC;
        """
        query_params = dict(slack_team_id=slack_team_id)
        with Database.connect(data_source_name=self.data_source_name) as connection:
            with Database.create_cursor(connection=connection) as cursor:
                cursor.execute(query, query_params)
                response = cursor.fetchall()

        return [Goal(**goal) for goal in response]
