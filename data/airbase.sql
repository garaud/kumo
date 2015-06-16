
-- Create the measure table
CREATE TABLE stations (
    id          serial PRIMARY KEY,
    code        VARCHAR (8) UNIQUE NOT NULL,
    country     VARCHAR (50) NOT NULL,
    height      INTEGER,
    lat         FLOAT NOT NULL,
    lon         FLOAT NOT NULL,
    name        VARCHAR (100) NOT NULL,
    type        VARCHAR (10)
);

COPY stations FROM './airbase.csv' DELIMITER ',' CSV;
-- CREATE EXTENSION postgis;
-- SELECT AddGeometryColumn ('stations', 'coordinate', 4326, 'POINT', 2);
-- SELECT ST_MakePoint(lat,lon) FROM stations;
