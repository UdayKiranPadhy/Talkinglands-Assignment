from typing import Optional
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor

from app.models.point import Latitude, Longitude, Point


class PointsRepository:
    POINTS_TABLE = "points"

    conn: connection

    def __init__(self, connection: connection) -> None:
        self.conn = connection
        if self.conn.closed:
            raise ValueError("Connection must be open")

    def __del__(self) -> None:
        if not self.conn.closed:
            self.conn.close()

    def get_point_based_on_latitude_and_longitude(
        self, latitude: Latitude, longitude: Longitude
    ) -> Optional[Point]:
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(  # type: ignore
                    f"SELECT id, point_name, ST_X(location) AS longitude, ST_Y(location) AS latitude  FROM {self.POINTS_TABLE} WHERE location = ST_SetSRID(ST_MakePoint(%s, %s), 4326)",
                    (longitude, latitude),
                )
                result = cursor.fetchone()
                if result:
                    return Point(**result)
        except Exception as e:
            print(f"Error fetching point: {e}")
        
        return None
