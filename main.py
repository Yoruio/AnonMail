from flask import current_app, flash, Flask, Markup, redirect, render_template, jsonify, session, Response
from flask import request, url_for
from google.cloud import error_reporting
import google.cloud.logging
import json
import logging

import bcrypt
from namecom import Auth, DnsApi\

from firestore import *

# setup logging
client = google.cloud.logging.Client()
client.get_default_handler()
client.setup_logging()

#get name.com key (unused currently)
with open('nameComKey', 'r') as file:
    DNSKEY = file.readline()


# setup flask
app = Flask(__name__)
app.secret_key = '\x16\xbe8\xff\x0e\xed;\x80\x8d\xec3R.\xc3\x7f\xfdN\xc7\xb4&\xdc3\xa9'
app.config['SESSION_TYPE'] = 'redis'

app.debug = False
app.testing = False

# homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    return '<h1>{}</h1>'.format(DNSKEY)

# receive API - emails sent here!
@app.route('/receive', methods=['GET', 'POST'])
def receive():
    email_json = request.get_json()
    add_email_json("last-raw-json", str(email_json))
    received_to = email_json['to']['value'][0]['address']
    received_from = email_json['from']['value'][0]['address']
    logging.info("received email from {} to {}".format(received_from, received_to))
    add_email_json(received_to, str(email_json))
    
    return Response(status=200)

# gunicorn stuff
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)