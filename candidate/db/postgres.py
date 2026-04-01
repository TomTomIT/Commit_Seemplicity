from typing import Any
import psycopg2
from psycopg2.extras import RealDictCursor
from config import settings

class PostgresClient:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            host=settings.db_host,
            port=settings.db_port,
            dbname=settings.db_name,
            user=settings.db_user,
            password=settings.db_password,
            cursor_factory=RealDictCursor,
        )

    def close(self) -> None:
        self.conn.close()

    def fetch_one(self, query: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()

    def get_finding(self, finding_id: int) -> dict[str, Any] | None:
        return self.fetch_one(
            "SELECT id, asset_id, vulnerability_id, status, detected_at, resolved_at, scanner, notes, is_dismissed "
            "FROM findings WHERE id = %s",
            (finding_id,),
        )

    def get_asset(self, asset_id: int) -> dict[str, Any] | None:
        return self.fetch_one(
            "SELECT id, hostname, ip_address, asset_type, environment, os, is_active FROM assets WHERE id = %s",
            (asset_id,),
        )

    def get_vulnerability(self, vulnerability_id: int) -> dict[str, Any] | None:
        return self.fetch_one(
            "SELECT id, cve_id, title, severity, cvss_score FROM vulnerabilities WHERE id = %s",
            (vulnerability_id,),
        )

    def count_findings_for_asset(self, asset_id: int) -> int:
        row = self.fetch_one("SELECT COUNT(*) AS count FROM findings WHERE asset_id = %s", (asset_id,))
        return int(row["count"]) if row else 0

    def count_findings_for_asset_vulnerability(self, asset_id: int, vulnerability_id: int) -> int:
        row = self.fetch_one(
            "SELECT COUNT(*) AS count FROM findings WHERE asset_id = %s AND vulnerability_id = %s",
            (asset_id, vulnerability_id),
        )
        return int(row["count"]) if row else 0
