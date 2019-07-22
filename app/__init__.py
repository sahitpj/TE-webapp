from flask import Flask
from flask_cors import CORS, cross_origin

app_flask = Flask(__name__)
CORS(app_flask, support_credentials=True)

# app_flask.secret_key = b'fdjjkgnuierhfuihuihedi'
from app import routes
from app import config_routes