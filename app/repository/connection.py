from __future__ import annotations
from typing import Any, Dict
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection as Connection


class ConnectionFactory:
    host: str
    user: str
    password: str
    defer_connect: bool = True

    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        defer_connect: bool = True,
    ):
        self.host = host
        self.user = user
        self.password = password
        self.defer_connect = defer_connect

    def connect(
        self, database: str | None = None, schema: str | None = None
    ) -> Connection:
        conn_params: Dict[str, Any] = {
            "host": self.host,
            "user": self.user,
            "password": self.password,
            "dbname": database,
            "cursor_factory": RealDictCursor,
        }

        # Set schema if provided via options parameter
        if schema:
            conn_params["options"] = f"-c search_path={schema},public"
        
        return psycopg2.connect(**conn_params)
