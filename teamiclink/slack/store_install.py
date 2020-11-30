from dataclasses import dataclass
from teamiclink.slack.model import TeamiclinkBot
from teamiclink.database import Database
from datetime import datetime


@dataclass
class TeamiclinkInstallStore:
    data_source_name: str

    def create_bot(
        self,
        team_id: str,
        bot_token: str,
        bot_id: str,
        bot_user_id: str,
        installed_at: datetime,
    ) -> TeamiclinkBot:
        query = """
            INSERT INTO teamiclink.slack_bot(team_id, bot_token, bot_id, bot_user_id, installed_at)
            VALUES (
                %(team_id)s, %(bot_token)s, %(bot_id)s, %(bot_user_id)s, %(installed_at)s)
            RETURNING id, team_id, bot_token, bot_id, bot_user_id, installed_at;
        """
        query_params = dict(
            team_id=team_id,
            bot_token=bot_token,
            bot_id=bot_id,
            bot_user_id=bot_user_id,
            installed_at=installed_at,
        )
        with Database.connect(data_source_name=self.data_source_name) as connection:
            with Database.create_cursor(connection=connection) as cursor:
                cursor.execute(query, query_params)
                response = cursor.fetchone()

        return TeamiclinkBot(**response)
