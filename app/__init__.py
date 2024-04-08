
from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = 'casestudy'
    app.config['SESSION_TYPE'] = 'filesystem'


    CORS(app, supports_credentials=True, origins="*")

    from app.api.routes import api_blueprint
    app.register_blueprint(api_blueprint)

    return app