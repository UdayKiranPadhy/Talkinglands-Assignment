-- Connect to the spatial_db database
\c spatial_db;


-- Create a new schema for spatial data
CREATE SCHEMA IF NOT EXISTS spatial_data;

-- Enable PostGIS extensions
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create a sample spatial table in the new schema
CREATE TABLE spatial_data.points (
    id SERIAL PRIMARY KEY,
    point_name VARCHAR(100),
    location GEOMETRY(Point, 4326),
    CONSTRAINT unique_location UNIQUE(location)
);

-- Insert some sample data
INSERT INTO spatial_data.points (point_name, location) VALUES 
    ('Seattle', ST_SetSRID(ST_MakePoint(-122.3321, 47.6062), 4326)),
    ('New York', ST_SetSRID(ST_MakePoint(-74.0060, 40.7128), 4326)),
    ('London', ST_SetSRID(ST_MakePoint(-0.1278, 51.5074), 4326)),
    ('Paris', ST_SetSRID(ST_MakePoint(2.3522, 48.8566), 4326)),
    ('Tokyo', ST_SetSRID(ST_MakePoint(139.6917, 35.6895), 4326));

-- Create a spatial index
CREATE INDEX points_location_idx ON spatial_data.points USING GIST (location);

-- Create an index on id (though typically not needed as it's already indexed by primary key)
CREATE INDEX points_id_idx ON spatial_data.points (id);

-- Example query to extract latitude and longitude:
-- SELECT point_name, ST_X(location) AS longitude, ST_Y(location) AS latitude FROM spatial_data.points;

-- Example queries to find points by latitude and longitude:

-- 1. Find a point at exact coordinates (may not use spatial index efficiently)
-- SELECT * FROM spatial_data.points 
-- WHERE ST_X(location) = -74.0060 AND ST_Y(location) = 40.7128;

-- 1b. Better alternative using index-optimized approach
-- SELECT * FROM spatial_data.points 
-- WHERE location = ST_SetSRID(ST_MakePoint(-74.0060, 40.7128), 4326);

-- Create a sample polygon table
CREATE TABLE spatial_data.regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    geom GEOMETRY(Polygon, 4326)
);

-- Insert some sample polygon data
INSERT INTO spatial_data.regions (name, geom) VALUES
    ('Region 1', ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY[
        ST_MakePoint(-122.3, 47.6),
        ST_MakePoint(-122.3, 47.7),
        ST_MakePoint(-122.2, 47.7),
        ST_MakePoint(-122.2, 47.6),
        ST_MakePoint(-122.3, 47.6)
    ])), 4326)),
    ('Region 2', ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY[
        ST_MakePoint(-74.0, 40.7),
        ST_MakePoint(-74.0, 40.8),
        ST_MakePoint(-73.9, 40.8),
        ST_MakePoint(-73.9, 40.7),
        ST_MakePoint(-74.0, 40.7)
    ])), 4326));

-- Create a spatial index for regions
CREATE INDEX regions_geom_idx ON spatial_data.regions USING GIST (geom);