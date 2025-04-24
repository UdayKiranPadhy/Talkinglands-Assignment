from pydantic import BaseModel
from typing import List, NewType, Dict, Any, Tuple


PolygonId = NewType("PolygonId", int)

class Polygon(BaseModel):
    id: PolygonId | None = None
    name: str
    coordinates: List[List[Tuple[float, float]]]
    
    def get_Geo_Json(self) -> Dict[str, Any]:
        json_coordinates: List[List[List[float]]] = []
        for ring in self.coordinates:
            json_ring = [[x, y] for x, y in ring]
            json_coordinates.append(json_ring)
            
        return {
            "type": "Polygon",
            "coordinates": json_coordinates
        }
