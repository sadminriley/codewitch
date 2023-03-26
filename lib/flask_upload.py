#!/usr/bin/env python3.11
import dockerops
import helpers
import komposer
import os
import platform
import secrets
import subprocess
from decouple import config as decouple_config
from flask import Flask, flash, jsonify, request, redirect, render_template, url_for
from flask_basicauth import BasicAuth
from werkzeug.utils import secure_filename


# Only allow yml/yaml type uploads
UPLOAD_FOLDER = os.getcwd()

ALLOWED_EXTENSIONS = {'yml', 'yaml'}


# Init Flask app and settings. Set max upload size to 16MB
app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['SESSION_TYPE'] = 'filesystem'


if decouple_config('FLASK_USER') is not None:
    print('FLASK_USER is %s' % decouple_config('FLASK_USER'))
    app.config['BASIC_AUTH_USERNAME'] = decouple_config('FLASK_USER')


if decouple_config('FLASK_PASS') is not None:
    print('FLASK_PASS is %s' % decouple_config('FLASK_PASS'))
    app.config['BASIC_AUTH_PASSWORD'] = decouple_config('FLASK_PASS')


if decouple_config('SECRET_KEY') is None:
    print('SECRET_KEY not found...creating \n')
else:
    HEX_KEY = secrets.token_urlsafe(16)
    app.config['SECRET_KEY'] = HEX_KEY
    print(f'SECRET_KEY is {HEX_KEY}')


basic_auth = BasicAuth(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Flask stuff starts below. Add auth stuff later on routes.

@app.route('/', methods=['GET'])
def health_check():
    response = jsonify(success=True)
    return response


# Kompose conversion routes

@app.route('/kompose/install')
def kompose_install():
    out = komposer.check_kompose()
    return jsonify(success=True)


@app.route('/kompose')
def kompose():
    out = dockerops.docker_kompose()
    return jsonify(success=True)


@app.route('/kompose/json')
def kompose_json():
    out = dockerops.docker_kompose(json_conversion=True)
    return jsonify(success=True)


@app.route('/kompose/helm')
def kompose_helm():
    out = dockerops.docker_kompose(helm=True)
    return jsonify(success=True)


@app.route('/kompose/replication')
def kompose_replication():
    # Also will accept repc_replicas count in a future upload. Defaults to 1 currently.
    out = dockerops.docker_kompose(repc=True)
    return jsonify(success=True)


@app.route('/kompose/daemonset')
def kompose_daemonset():
    out = dockerops.docker_kompose(daemonset=True)
    return jsonify(success=True)


@app.route('/kompose/statefulset')
def kompose_statefulset():
    out = dockerops.docker_kompose(statefulset=True)
    return jsonify(success=True)


# Kube routes
@app.route('/kube/apply')
def kube_apply():
    out = dockerops.kubectl_apply()
    return jsonify(success=True)


# Use basic auth for user/pass for flask
@app.route('/upload', methods=['GET', 'POST'])
@basic_auth.required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename. Fix this later.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', name=filename))
    return '''
    <!doctype html>
    <style>
    body {
      color-scheme: dark;
      background-color: rgb(22 46 22);
      font-family: 'Comic Sans MS' !important;
    }

    button {
      height: 2em;
      min-width: 3.236em; border-radius: 25em;
      border-width: 0;
      color: roba (255, 255,255, .78);
      background-color: rgba(150, 150, 150, .5);
      font-size: 1.5em;
    }

    </style>
    <title>Upload docker-compose.yml,yaml file</title>
    <h1 style="color: #5a4aa0;">Upload new Docker Compose file
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
     </body>
    </h1>

    '''



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
