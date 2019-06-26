from flask import redirect, render_template, jsonify, request, make_response, abort, g, session, Response
from flask_cors import CORS, cross_origin

from app import app_flask

@app_flask.route('/', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def Hello():
    return "Hello"
