import json
from typing import Optional, Dict, List, Tuple
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from app.models.polygon import Polygon


class PolygonRepository:
    REGIONS_TABLE = "regions"
    
    conn: connection

    def __init__(self, connection: connection) -> None:
        self.conn = connection
        if self.conn.closed:
            raise ValueError("Connection must be open")

    def __del__(self) -> None:
        if not self.conn.closed:
            self.conn.close()

    def find_by_id(self, polygon_id: int) -> Optional[Polygon]:

        query = """
            SELECT id, name, ST_AsGeoJSON(geom)::json as geom
            FROM regions 
            WHERE id = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (polygon_id,)) # type: ignore
            result = cursor.fetchone()
            if result:
                polygon_geometry = self._convert_geojson_to_list(result['geom'])
                result['coordinates'] = polygon_geometry

                return Polygon(**result)
        return None
    
    def _convert_geojson_to_list(self, geojson: Dict[str, str | List[List[List[float]]]]) -> List[List[Tuple[float, float]]]:
        """
        Convert GeoJSON to a list of coordinates.
        """
        if geojson['type'] == 'Polygon':
            if isinstance(geojson['coordinates'], list):
                coordinates = geojson['coordinates']
                return [[(coord[0], coord[1]) for coord in ring] for ring in coordinates]
        raise ValueError("Invalid GeoJSON format")

    def create(self, polygon: Polygon) -> Polygon:
        
        query = """
            INSERT INTO regions (name, geom) 
            VALUES (%s, ST_GeomFromGeoJSON(%s))
            RETURNING id, name, ST_AsGeoJSON(geom)::json as geometry
        """
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, ( # type: ignore
                polygon.name, 
                json.dumps(polygon.get_Geo_Json())
            ))
            result = cursor.fetchone()
            self.conn.commit()
            if result:
                polygon_geometry = self._convert_geojson_to_list(result['geometry'])
                result['coordinates'] = polygon_geometry
                return Polygon(**result)
        raise Exception("Failed to create polygon")

    def update(self, polygon_id: int, polygon: Polygon) -> Optional[Polygon]:
        
        query = """
            UPDATE regions 
            SET name = %s, 
                geom = ST_GeomFromGeoJSON(%s)
            WHERE id = %s
            RETURNING id, name, ST_AsGeoJSON(geom)::json as geometry
        """
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, ( # type: ignore
                polygon.name, 
                json.dumps(polygon.get_Geo_Json()),
                polygon_id
            ))
            result = cursor.fetchone()
            self.conn.commit()
            if result:
                polygon_geometry = self._convert_geojson_to_list(result['geometry'])
                result['coordinates'] = polygon_geometry
                return Polygon(**result)
        raise Exception("Failed to update polygon")


    def delete(self, polygon_id: int) -> bool:
        query = """
            DELETE FROM regions 
            WHERE id = %s
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, (polygon_id,))
            self.conn.commit()
            return cursor.rowcount > 0
