from typing import Optional, Dict
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

    def get_point_based_on_point_id(self, point_id: int) -> Optional[Point]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(  # type: ignore
                f"SELECT id, point_name, ST_X(location) AS longitude, ST_Y(location) AS latitude FROM {self.POINTS_TABLE} WHERE id = %s",
                (point_id,),
            )
            result = cursor.fetchone()
            if result:
                return Point(**result)

    def delete_point(self, point_id: int) -> bool:
        with self.conn.cursor() as cursor:
            cursor.execute(  # type: ignore
                f"DELETE FROM {self.POINTS_TABLE} WHERE id = %s",
                (point_id,),
            )
            self.conn.commit()
            return cursor.rowcount > 0

    def create_point(self, point: Point) -> Point:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(  # type: ignore
                f"INSERT INTO {self.POINTS_TABLE} (point_name, location) VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326)) RETURNING id",
                (point.point_name, point.longitude, point.latitude),
            )
            result = cursor.fetchone()
            if result is None:
                raise Exception("Failed to create point")
            point_id = result["id"]
            self.conn.commit()
            return Point(id=point_id, **point.model_dump(exclude={"id"}))

    def update_point(self, point_id: int, update_data: Dict[str, str | float]) -> bool:
        try:
            if not update_data:
                return True

            query = "UPDATE points SET "
            values: list[str | float] = []

            if "point_name" in update_data:
                query += "point_name = %s "
                values.append(update_data["point_name"])
                if len(update_data) > 1:
                    query += ", "
            if "latitude" in update_data and "longitude" in update_data:
                query += "location = ST_SetSRID(ST_MakePoint(%s, %s), 4326) "
                values.append(update_data["longitude"])
                values.append(update_data["latitude"])

            query += " WHERE id = %s"
            values.append(point_id)

            # Execute the update query
            with self.conn.cursor() as cursor:
                cursor.execute(query, values)
                self.conn.commit()

                return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Error updating point: {e}")
            return False
