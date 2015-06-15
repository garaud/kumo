# coding: utf-8

import psycopg2


DBNAME = "kumo"


def jsonize(query_result):
    """Turn a query result to a dict
    """
    res = []
    for station_id,name,country,species,pos,height in query_result:
        res.append({'id': station_id,
                    'name': name,
                    'country': country,
                    'species': species,
                    'pos': pos,
                    'height': height})
    return res

def station(by_id):
    cnx = psycopg2.connect("dbname={}".format(DBNAME))
    with cnx.cursor() as cur:
        cur.execute("SELECT * FROM stations WHERE id =  %(station_id)s;",
                    {'station_id': by_id})
        return cur.fetchall()

def countries(limit=100):
    cnx = psycopg2.connect("dbname={}".format(DBNAME))
    with cnx.cursor() as cur:
        cur.execute("SELECT DISTINCT country FROM stations ORDER BY country ASC LIMIT %s ;" % limit)
        return [x[0] for x in cur.fetchall()]

def stations(limit=100):
    cnx = psycopg2.connect("dbname={}".format(DBNAME))
    with cnx.cursor() as cur:
        cur.execute("SELECT * FROM stations LIMIT %s;" % limit)
        return cur.fetchall()

def by_country(name):
    cnx = psycopg2.connect("dbname={}".format(DBNAME))
    with cnx.cursor() as cur:
        cur.execute("SELECT * FROM stations WHERE country = %(name)s",
                    {'name': name.capitalize()})
        return cur.fetchall()
