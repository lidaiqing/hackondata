from __future__ import absolute_import
from flask import Blueprint
from flask.ext.cors import CORS
from flask_restful import Api
from flask_restful_swagger import swagger
from . import attraction
api_bp = Blueprint(
    'api',
    __name__,
    template_folder='templates',
    static_folder='static')
CORS(api_bp)

api = swagger.docs(
    Api(api_bp),
    apiVersion='0.1',
    api_spec_url='/spec',
    swaggerVersion='2.0')

api.add_resource(attraction.AttractionGeoJson, '/attraction')
api.add_resource(attraction.AttractionPlace, '/attraction/<int:_id>')
