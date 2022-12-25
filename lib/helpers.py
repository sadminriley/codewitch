#!/usr/bin/env python3.11
import os
import platform
import subprocess
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


# Only allow yml/yaml type uploads
UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'yml', 'yaml'}


# Init Flask app and settings
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def install_kompose():
    platform_type = platform.uname()
    if 'Linux' in platform_type:
        if 'Ubuntu' in platform_type:
            subprocess.Popen("install_kompose_deb.sh", shell=True) # Installs 'Most' Linux distros
        elif 'Fedora' in platform_type:
            subprocess.Popen("install_kompose_redhat.sh", shell=True) # installs via DNF pkg manager
        else:
            print('Closing....\nunsupported platform type!')
            sys.exit(1)


# Something could be done here to make it accept requests from JSON??? or something
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload docker-compose.yml,yaml file</title>
    <h1>Upload new Docker Compose file</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


def run_kompose(file_name):
    # Log the run command output
    try:
        subprocess.run(["kompose", "konvert"])
    except subprocess.CalledProcessError as e:
        print(e.output)





if __name__ == '__main__':
    app.run(debug=True)
