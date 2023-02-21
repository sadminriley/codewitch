#!/usr/bin/env python3.11
import os
import platform
import subprocess
from decouple import config as decouple_config
from flask import Flask, flash, request, redirect, render_template, url_for
from flask_basicauth import BasicAuth
from werkzeug.utils import secure_filename


# Only allow yml/yaml type uploads
UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = {'yml', 'yaml'}


# Init Flask app and settings. Set max upload size to 16MB
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['SECRET_KEY'] = 'testkey'
app.config['SESSION_TYPE'] = 'filesystem'


if decouple_config('FLASK_USER') is not None:
    print('FLASK_USER is %s' % decouple_config('FLASK_USER'))
    app.config['BASIC_AUTH_USERNAME'] = decouple_config('FLASK_USER')


if decouple_config('FLASK_PASS') is not None:
    print('FLASK_PASS is %s' % decouple_config('FLASK_PASS'))
    app.config['BASIC_AUTH_PASSWORD'] = decouple_config('FLASK_PASS')


basic_auth = BasicAuth(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    <title>Upload docker-compose.yml,yaml file</title>
    <h1>Upload new Docker Compose file</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
