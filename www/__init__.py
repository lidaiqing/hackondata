from __future__ import absolute_import
from flask import Flask
from .models import mongo

def create_app(config_obj_path='config.base'):
    app = Flask(__name__)
    app.config.from_object(config_obj_path)
    mongo.init_app(app)
    from .views import views_bp
    app.register_blueprint(views_bp)
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/0.1')
    return app
