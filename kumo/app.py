# coding: utf-8

from collections import OrderedDict

from flask import Flask, Blueprint, jsonify
from flask.ext.restplus import Resource, fields, Api, apidoc

from kumo.query import (DEFAULT_LIMIT, station, stations, by_country,
                        to_geojson, countries, is_station_id)

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, ui=False, title='Kumo',
          description='API to request air quality measuring stations')
ns_station = api.namespace('stations', description='Get stations from ID')
ns_country = api.namespace('countries', description='Get stations from countries')

@blueprint.route('/doc/', endpoint='doc')
def swagger_ui():
    return apidoc.ui_for(api)

app.register_blueprint(blueprint)
app.register_blueprint(apidoc.apidoc)  # only needed for assets and templates

# Query parameters parser for /stations
stations_parser = api.parser()
stations_parser.add_argument('limit', type=int, required=False, location='args',
                             help='Query limit')
stations_parser.add_argument('type', type=str, required=False, location='args',
                             help='Type of the station: background, traffic, industrial or unknown')
stations_parser.add_argument('country', type=str, required=False, location='args',
                             help='Specify a country')
# Query parameters parser for /countries
countries_parser = api.parser()
countries_parser.add_argument('limit', type=int, required=False, location='args',
                              help='Query limit')
countries_parser.add_argument('type', type=str, required=False, location='args',
                              help='Type of the station: background, traffic, industrial or unknown')

def abort_if_not_station(station_id):
    """Raise 404 if the station ID is not found.
    """
    if not is_station_id(station_id):
        api.abort(404, "Station ID {} not found".format(station_id))

@ns_station.route('/')
class Stations(Resource):
    @api.doc(parser=stations_parser, description="Get all stations")
    def get(self):
        args = stations_parser.parse_args()
        limit = args['limit']
        limit = limit if limit is not None else DEFAULT_LIMIT
        return to_geojson(stations(limit=limit, country=args['country'],
                                   station_type=args['type']))

@ns_station.route('/<int:station_id>')
@api.doc(responses={404: "Station ID not found"},
         params={'station_id': "Station ID"})
class Station(Resource):
    @api.doc(description="Get station from ID")
    def get(self, station_id):
        abort_if_not_station(station_id)
        return to_geojson(station(station_id))

@ns_country.route('/')
class Countries(Resource):
    @api.doc(parser=countries_parser, description="Get countries")
    def get(self):
        args = countries_parser.parse_args()
        limit = args['limit']
        limit = limit if limit is not None else DEFAULT_LIMIT
        return countries(limit=limit)

@ns_country.route('/<string:name>')
@api.doc(responses={404: "Country not found"},
         params={'name': "Country"})
class Country(Resource):
    @api.doc(description="Get stations from a specific country")
    def get(self, name):
        args = countries_parser.parse_args()
        limit = args['limit']
        limit = limit if limit is not None else DEFAULT_LIMIT
        stations = by_country(name, limit=limit, station_type=args['type'])
        if not stations:
            api.abort(404, "Country {} not found".format(name))
        return to_geojson(stations)


if __name__ == '__main__':
    app.run(debug=True)
