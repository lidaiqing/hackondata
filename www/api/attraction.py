from flask_restful import fields, marshal_with, abort, marshal
from flask_restful import Resource
import pymongo
from ..models import mongo

class FixedField(fields.Raw):
    """docstring for ClassName"""
    def __init__(self, value):
        super(FixedField, self).__init__()
        self.value = value

    def output(self, key, obj):
        return self.value

ATTRACTION_COLLECTION = 'ATTRACTION'

ATTRACTION_FIELDS_MODEL = {
    'id': fields.Integer,
    'name': fields.String,
    'full_address': fields.String,
    'street_number': fields.String,
    'street_name': fields.String,
    'suite': fields.String,
    'city': fields.String,
    'province': fields.String,
    'postal_code': fields.String,
    'ward': fields.String,
    'performance': fields.String,
    'exhibition': fields.String,
    'screen': fields.String,
    'library': fields.String,
    'multipurpose': fields.String,
    'heritage': fields.String,
    'ownership': fields.String,
    'timestamp': fields.Integer,
    "coordinates": fields.List(fields.Float)
}


ATTRACTION_FIELDS_GEOJSON_MODEL = {
    "type":  FixedField("Feature"),
    "geometry": {
        "type":  FixedField("Point"),
        "coordinates": fields.List(fields.Float, attribute="coordinates")
    },
    "properties": {
        'id': fields.Integer,
        "name": fields.String,
        'full_address': fields.String,
        'street_number': fields.String,
        'street_name': fields.String,
        'suite': fields.String,
        'city': fields.String,
        'province': fields.String,
        'postal_code': fields.String,
        'ward': fields.String,
        'performance': fields.String,
        'exhibition': fields.String,
        'screen': fields.String,
        'library': fields.String,
        'multipurpose': fields.String,
        'heritage': fields.String,
        'ownership': fields.String,
        'timestamp': fields.Integer,
        "coordinates": fields.List(fields.Float)
    }
}


class AttractionGeoJson(Resource):

    def get(self):
        results = mongo.db[ATTRACTION_COLLECTION].find()
        results = [row for row in results]
        results = marshal(results, ATTRACTION_FIELDS_GEOJSON_MODEL)
        geojson = {
            'type': 'FeatureCollection',
            'features': results
        }
        return geojson, 200

class AttractionPlace(Resource):

    def get(self, _id):
        results = mongo.db[ATTRACTION_COLLECTION].find({'id': _id})
        results = [row for row in results]
        results = marshal(results, ATTRACTION_FIELDS_GEOJSON_MODEL)

        return results, 200
