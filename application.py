import logging
from flask import Flask, request
from flask_cors import CORS
import os, sys, json
import requests
import copy

application = Flask(__name__)
CORS(application)

logger = logging.getLogger("tattle-api")

@application.route('/health')
def health_check():
    logger.debug('<health-check>')
    return "OK"

@application.route('/upload_message', methods=['POST'])
def post_message():
    return 1

@application.route('/upload_image', methods=['POST'])
def post_image():
    data = requests.get_json(force=True)
    return 1

