from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import psycopg2.errors
from slack_sdk.oauth.installation_store import Bot, Installation, InstallationStore
from teamiclink.database import Database
from teamiclink.slack.errors import MissingBotError
from teamiclink.slack.model import TeamiclinkBot


@dataclass
class TeamiclinkInstallStore(InstallationStore):
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
                try:
                    cursor.execute(query, query_params)
                except psycopg2.errors.UniqueViolation:
                    return self.update_bot(
                        team_id=team_id,
                        bot_token=bot_token,
                        bot_id=bot_id,
                        bot_user_id=bot_user_id,
                    )
                response = cursor.fetchone()

        return TeamiclinkBot(**response)

    def read_bot(self, team_id: str) -> TeamiclinkBot:
        query = """
            SELECT id, team_id, bot_token, bot_id, bot_user_id, installed_at
            FROM teamiclink.slack_bot
            WHERE team_id=%(team_id)s;
        """
        query_params = dict(team_id=team_id)

        with Database.connect(data_source_name=self.data_source_name) as connection:
            with Database.create_cursor(connection=connection) as cursor:
                cursor.execute(query, query_params)
                response = cursor.fetchone()

        try:
            return TeamiclinkBot(**response)
        except TypeError:
            raise MissingBotError(f"bot missing for team {team_id}")

    def find_bot(
        self, *, team_id: Optional[str], enterprise_id: Optional[str] = None
    ) -> Optional[Bot]:
        assert team_id
        try:
            teamiclink_bot = self.read_bot(team_id=team_id)
        except MissingBotError:
            return None

        return Bot(
            team_id=teamiclink_bot.team_id,
            bot_token=teamiclink_bot.bot_token,
            bot_id=teamiclink_bot.bot_id,
            bot_user_id=teamiclink_bot.bot_user_id,
            installed_at=teamiclink_bot.installed_at.timestamp(),
        )

    def save(self, installation: Installation) -> None:
        assert installation.team_id
        self.create_bot(
            team_id=installation.team_id,
            bot_token=installation.bot_token,
            bot_id=installation.bot_id,
            bot_user_id=installation.bot_user_id,
            installed_at=datetime.now(timezone.utc),
        )

    def delete_bot(self, team_id: str) -> int:
        query = """
            DELETE FROM teamiclink.slack_bot
            WHERE team_id=%(team_id)s;
        """
        query_params = dict(team_id=team_id)
        with Database.connect(data_source_name=self.data_source_name) as connection:
            with Database.create_cursor(connection=connection) as cursor:
                cursor.execute(query, query_params)
        return cursor.rowcount

    def update_bot(
        self,
        team_id: str,
        bot_token: str,
        bot_id: str,
        bot_user_id: str,
    ) -> TeamiclinkBot:
        query = """
            UPDATE teamiclink.slack_bot
            SET
                bot_token=%(bot_token)s,
                bot_id=%(bot_id)s,
                bot_user_id=%(bot_user_id)s
            WHERE team_id=%(team_id)s
            RETURNING id, team_id, bot_token, bot_id, bot_user_id, installed_at;
        """
        query_params = dict(
            team_id=team_id,
            bot_token=bot_token,
            bot_id=bot_id,
            bot_user_id=bot_user_id,
        )
        with Database.connect(data_source_name=self.data_source_name) as connection:
            with Database.create_cursor(connection=connection) as cursor:
                cursor.execute(query, query_params)
                response = cursor.fetchone()

        return TeamiclinkBot(**response)
