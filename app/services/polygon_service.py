from typing import Optional
from app.repository.spatial_db.polygon import PolygonRepository
from app.models.polygon import Polygon


class PolygonService:

    def __init__(self, polygon_repository: PolygonRepository):
        self.repo = polygon_repository

    def get_polygon_by_id(self, polygon_id: int) -> Optional[Polygon]:
        return self.repo.find_by_id(polygon_id)

    def create_polygon(self, polygon: Polygon) -> Polygon:
        return self.repo.create(polygon)

    def update_polygon(self, polygon_id: int, polygon: Polygon) -> Optional[Polygon]:
        return self.repo.update(polygon_id, polygon)

    def delete_polygon(self, polygon_id: int) -> bool:
        return self.repo.delete(polygon_id)
