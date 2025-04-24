-- Enable PostGIS extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder;
CREATE EXTENSION IF NOT EXISTS postgis_raster;

-- Create a new schema for spatial data
CREATE SCHEMA IF NOT EXISTS spatial_data;

-- Create a sample spatial table in the new schema
CREATE TABLE spatial_data.points (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    geom GEOMETRY(Point, 4326)
);

-- Insert some sample data
INSERT INTO spatial_data.points (name, geom) VALUES 
    ('Point 1', ST_SetSRID(ST_MakePoint(-122.3321, 47.6062), 4326)),
    ('Point 2', ST_SetSRID(ST_MakePoint(-74.0060, 40.7128), 4326)),
    ('Point 3', ST_SetSRID(ST_MakePoint(-0.1278, 51.5074), 4326)),
    ('Point 4', ST_SetSRID(ST_MakePoint(2.3522, 48.8566), 4326)),
    ('Point 5', ST_SetSRID(ST_MakePoint(139.6917, 35.6895), 4326));

-- Create a spatial index
CREATE INDEX points_geom_idx ON spatial_data.points USING GIST (geom);

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

$$ LANGUAGE plpgsql;