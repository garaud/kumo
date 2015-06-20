# coding: utf-8

"""Kumo: REST API for requesting air quality measuring stations
"""


def geojson(query_result):
    """Turn a SQL query result to a GeoJSONisable dict

    http://geojson.org/geojson-spec.html
    """
    res = []
    for station_id,code,country,height,lat,lon,name,station_type in query_result:
        res.append({
            "geometry": {
                "coordinates": [lon,lat],
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
    return {'features': res, "type": "FeatureCollection"}
