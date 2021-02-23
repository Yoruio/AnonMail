from flask import current_app, flash, Flask, Markup, redirect, render_template, jsonify, session
from flask import request, url_for
from google.cloud import error_reporting
import google.cloud.logging

import bcrypt
from namecom import Auth, DnsApi

with open('nameComKey', 'r') as file:
    DNSKEY = file.readline()


app = Flask(__name__)
app.secret_key = '\x16\xbe8\xff\x0e\xed;\x80\x8d\xec3R.\xc3\x7f\xfdN\xc7\xb4&\xdc3\xa9'
app.config['SESSION_TYPE'] = 'redis'

app.debug = False
app.testing = False

@app.route('/', methods=['GET', 'POST'])
def index():
    return '<h1>{}</h1>'.format(DNSKEY)

@app.route('/receive', methods=['GET', 'POST'])
def receive():
    with open('received.txt', 'a') as file:
        file.write(str(request.get_json()))
    return 'success'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)