from typing import NewType
from pydantic import BaseModel, Field

PointId = NewType("PointId", str)
Latitude = NewType("Latitude", float)
Longitude = NewType("Longitude", float)


class Point(BaseModel):
    """Model representing a geographic point with latitude and longitude."""

    id: PointId = Field(..., description="Latitude of the point")
    point_name: str = Field(..., description="Name of the point")
    latitude: Latitude = Field(..., description="Latitude of the point")
    longitude: Longitude = Field(..., description="Longitude of the point")
