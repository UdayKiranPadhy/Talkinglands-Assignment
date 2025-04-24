from typing import NewType
from pydantic import BaseModel, Field

PointId = NewType("PointId", int)
Latitude = NewType("Latitude", float)
Longitude = NewType("Longitude", float)


class Point(BaseModel):
    """Model representing a geographic point with latitude and longitude."""

    point_name: str = Field(..., description="Name of the point")
    latitude: Latitude = Field(..., description="Latitude of the point")
    longitude: Longitude = Field(..., description="Longitude of the point")
    id: PointId | None = Field(None, description="ID of the point")
