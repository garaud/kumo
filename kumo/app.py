# coding: utf-8

from collections import OrderedDict

from flask import Flask, jsonify
from flask_restful import Resource, Api

from kumo.query import (station, stations, by_country, jsonize, countries)

app = Flask(__name__)
api = Api(app)

class Station(Resource):
    def get(self, station_id):
        jsonize(station(station_id))

class Stations(Resource):
    def get(self):
        return jsonize(stations())

class Countries(Resource):
    def get(self):
        return countries()

class Country(Resource):
    def get(self, name):
        return jsonize(by_country(name))

api.add_resource(Stations, '/stations')
api.add_resource(Station, '/stations/<int:station_id>')
api.add_resource(Countries, '/countries')
api.add_resource(Country, '/countries/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)
