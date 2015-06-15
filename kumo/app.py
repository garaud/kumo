# coding: utf-8

from collections import OrderedDict

from flask import Flask, Blueprint, jsonify
from flask.ext.restplus import Resource, fields, Api, apidoc

from kumo.query import (station, stations, by_country, jsonize, countries,
                        is_station_id)

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, ui=False, title='Kumo',
          description='Air quality measures stations')
ns_station = api.namespace('stations', description='Get stations from ID')
ns_country = api.namespace('countries', description='Get stations from countries')

@blueprint.route('/doc/', endpoint='doc')
def swagger_ui():
    return apidoc.ui_for(api)

app.register_blueprint(blueprint)
app.register_blueprint(apidoc.apidoc)  # only needed for assets and templates

def abort_if_not_station(station_id):
    if not is_station_id(station_id):
        api.abort(404, "Station ID {} not found".format(station_id))

@ns_station.route('/')
class Stations(Resource):
    @api.doc(description="Get all stations")
    def get(self):
        return jsonize(stations())

@ns_station.route('/<int:station_id>')
@api.doc(responses={404: "Station ID not found"},
         params={'station_id': "Station ID"})
class Station(Resource):
    @api.doc(description="Get station from ID")
    def get(self, station_id):
        abort_if_not_station(station_id)
        return jsonize(station(station_id))

@ns_country.route('/')
class Countries(Resource):
    @api.doc(description="Get countries")
    def get(self):
        return countries()

@ns_country.route('/<string:name>')
@api.doc(responses={404: "Country not found"},
         params={'name': "Country"})
class Country(Resource):
    @api.doc(description="Get stations from a specific country")
    def get(self, name):
        return jsonize(by_country(name))


if __name__ == '__main__':
    app.run(debug=True)
