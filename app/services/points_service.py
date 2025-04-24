from typing import Optional
from app.models.point import Latitude, Longitude, Point
from app.repository.spatial_db.points import PointsRepository


class PointsService:
    """Service class for managing points data"""

    def __init__(self, points_repository: PointsRepository):
        self.repo = points_repository

    def get_point_based_on_latitude_and_longitude(
        self, latitude: Latitude, longitude: Longitude
    ) -> Optional[Point]:
        point_data = self.repo.get_point_based_on_latitude_and_longitude(
            latitude, longitude
        )

        return point_data

    def get_point_based_on_point_id(self, point_id: int) -> Optional[Point]:
        point_data = self.repo.get_point_based_on_point_id(point_id)

        return point_data

    def delete_point(self, point_id: int) -> bool:
        return self.repo.delete_point(point_id)

    def create_point(self, point: Point) -> Point:
        return self.repo.create_point(point)

    def update_point(
        self,
        point_id: int,
        point_name: Optional[str] = None,
        latitude: Optional[Latitude] = None,
        longitude: Optional[Longitude] = None,
    ) -> Optional[Point]:
        point = self.get_point_based_on_point_id(point_id)
        if not point:
            return None

        # Update only the fields that were provided
        update_data: dict[str, str | float] = {}
        if point_name is not None:
            update_data["point_name"] = point_name
        if latitude and longitude:
            update_data["latitude"] = latitude
            update_data["longitude"] = longitude

        if update_data:
            # Execute the update
            self.repo.update_point(point_id, update_data)

            # Return the updated point
            return self.get_point_based_on_point_id(point_id)

        return point
