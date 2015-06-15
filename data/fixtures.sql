
-- Create the measure table
CREATE TABLE stations (
    id serial PRIMARY KEY,
    name     VARCHAR (20) UNIQUE NOT NULL,
    country  VARCHAR (50) NOT NULL,
    species  VARCHAR (8),
    location point NOT NULL,
    height   FLOAT
);


-- Populate it with fake data
INSERT INTO stations (name, country, species, location, height)
    VALUES ('FRGIR33', 'France', 'O3', '(44.8,-0.57)', 50.6);
INSERT INTO stations (name, country, species, location, height)
    VALUES ('FRILD07', 'France', 'PM10', '(48.51,2.20)', 250.6);
INSERT INTO stations (name, country, species, location, height)
    VALUES ('GEBER03', 'Germany', 'SOX', '(52.30,13.25)', 324.5);
INSERT INTO stations (name, country, species, location, height)
    VALUES ('SPBAR64', 'Spain', 'O3', '(41.23,-2.1)', 25.3);
