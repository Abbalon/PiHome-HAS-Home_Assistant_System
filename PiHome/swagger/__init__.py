#!venv/bin/python3
# -*- code: utf-8 -*-
"""Fichero para implementar Swagger"""
import os

from flask import Blueprint, jsonify

swagger_ctr = Blueprint('api', __name__, url_prefix='/api')

# Create an APISpec
specs = {
    "swagger": "2.0",
    "info": {
        "title": "PiHome Swagger",
        "description": "RESTfull API for admin test",
        "version": "1.0.0",
        "contact": {
            "name": "Montbs",
            "email": "PiDomoticTFG+contact@gmail.com ",
            "url": "https://github.com/Abbalon",
        }
    },
    "host": "localhost:5000",  # overrides localhost:500
    # "basePath": "/swagger/",  # base bash for blueprint registration
    "schemes": [
        "http"
    ]
}


@swagger_ctr.route('/test', methods=['GET'])
def test():
    """
    Get info on our server
    ---
    get:
      description: Get the version information for our service
      responses:
        200:
          content:
            application/json:
             schema:
               type: object
               properties:
                 version:
                   type: string
                   description: Version number of our service
    """
    return jsonify({"version": "TOP", })


@swagger_ctr.route("/spec", methods=['GET'])
def spec():
    return jsonify({"version": os.environ.get("VERSION"), })
