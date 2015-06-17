# coding: utf-8

import psycopg2


DBNAME = "kumo"
DEFAULT_LIMIT = 100


def to_geojson(query_result):
    """Turn a SQL query result to a GeoJSONisable dict

    http://geojson.org/geojson-spec.html
    """
    res = []
    for station_id,code,country,height,lat,lon,name,station_type in query_result:
        res.append({
            "geometry": {
                "coordinates": [lat,lon],
                "type": "Point"
            },
            "properties": {
                "code": code,
                "country": country,
                "height": height,
                "id": station_id,
                "name": name,
                "type": station_type
            },
            "type": "Feature"})
    return {'features': res}


def is_station_id(station_id):
    cnx = psycopg2.connect("dbname={}".format(DBNAME))
    with cnx.cursor() as cur:
        cur.execute("SELECT last_value FROM stations_id_seq;")
        last_value = cur.fetchone()[0]
    return station_id <= last_value

def is_country(country):
    return country in countries()

def station(by_id):
    cnx = psycopg2.connect("dbname={}".format(DBNAME))
    with cnx.cursor() as cur:
        cur.execute("SELECT * FROM stations WHERE id =  %(station_id)s;",
                    {'station_id': by_id})
        return cur.fetchall()

def stations(limit=DEFAULT_LIMIT, country=None, station_type=None):
    cnx = psycopg2.connect("dbname={}".format(DBNAME))
    query = ["SELECT * FROM stations"]
    params = {}
    if country is not None:
        params['country'] = country
        query.append(" country = %(country)s")
    if station_type is not None:
        params['type'] = station_type
        query.append(" type  = %(species)s")
    query_limit = " LIMIT %s" % limit
    if len(query) > 1:
        query = query[0] + ' WHERE ' + 'AND'.join(query[1:])
    else:
        query = query[0]
    query += query_limit
    with cnx.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()

def countries(limit=DEFAULT_LIMIT):
    cnx = psycopg2.connect("dbname={}".format(DBNAME))
    with cnx.cursor() as cur:
        cur.execute("SELECT DISTINCT country FROM stations ORDER BY country LIMIT %s;" % limit)
        return [x[0] for x in cur.fetchall()]

def by_country(name):
    cnx = psycopg2.connect("dbname={}".format(DBNAME))
    with cnx.cursor() as cur:
        cur.execute("SELECT * FROM stations WHERE country = %(name)s",
                    {'name': name.capitalize()})
        return cur.fetchall()

def species(limit=DEFAULT_LIMIT):
    cnx = psycopg2.connect("dbname={}".format(DBNAME))
    with cnx.cursor() as cur:
        cur.execute("SELECT DISTINCT species FROM stations ORDER BY species ASC LIMIT %s ;" % limit)
        return [x[0] for x in cur.fetchall()]

def by_species(name):
    cnx = psycopg2.connect("dbname={}".format(DBNAME))
    with cnx.cursor() as cur:
        cur.execute("SELECT * FROM stations WHERE species = %(name)s",
                    {'name': name})
        return cur.fetchall()
