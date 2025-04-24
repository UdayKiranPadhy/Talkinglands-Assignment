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
