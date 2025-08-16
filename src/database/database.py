import os
import psycopg2, psycopg2.extras, psycopg2.sql

from typing import Dict, List, Optional, Tuple

SCHEMA_NAME = "ggsimao_aiqfome"


class _Database:
    initialized = False

    @classmethod
    def initialize(cls):
        if cls.initialized:
            return

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "postgres"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "new_password"),
            port=int(os.getenv("DB_PORT", 5432)),
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}")
        cur.execute(f"SET search_path TO {SCHEMA_NAME}")

        with open("schema.sql", "r") as f:
            schema_sql = f.read()

        cur.execute(schema_sql)

        cur.close()
        conn.close()

        cls.initialized = True


class DBConn:
    def __enter__(self):
        if not _Database.initialized:
            _Database.initialize()

        self._conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "postgres"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "new_password"),
            port=int(os.getenv("DB_PORT", 5432)),
            options=f"-c search_path={SCHEMA_NAME}",
        )
        self._cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._conn.commit()
        else:
            self._conn.rollback()
        self._cur.close()
        self._conn.close()

    def execute_query(
        self, query: str, params: Optional[Tuple], returns=False
    ) -> Optional[List[Dict]]:
        self._cur.execute(query, params)
        resp = self._cur.fetchall() if returns else None
        return resp
