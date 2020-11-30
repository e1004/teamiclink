from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor


class Database:
    @classmethod
    @contextmanager
    def connect(_, data_source_name: str):
        connection = psycopg2.connect(dsn=data_source_name)

        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    @classmethod
    @contextmanager
    def create_cursor(_, connection):
        try:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            yield cursor
        finally:
            cursor.close()
