#!/usr/bin/env python3.11
# Kompose related functions
import os
import platform
import subprocess
import sys


DISTRO_INFO = str(os.uname())


KOMPOSE_PATH = "/usr/local/bin/kompose"


# Check for existing kompose install, installs it otherwise
def check_kompose():
    if not os.path.exists(KOMPOSE_PATH):
        install_kompose()
    else:
        print("\n %s already found. Not installing. \n" % KOMPOSE_PATH)


def install_kompose():
    if 'Ubuntu' in DISTRO_INFO:
        install_process = subprocess.Popen("./install_kompose_deb.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Installs 'Most' Linux distros
        success, install_error = install_process.communicate()
        if not install_error:
            print('Install complete', success.decode())
        else:
            print('Error!', install_error.decode())
    elif 'Fedora' in DISTRO_INFO:
        install_process = subprocess.Popen("./install_kompose_redhat.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # installs via DNF pkg manager
        success, install_error = install_process.communicate()
        if not install_error:
            print('Install complete', success.decode())
        else:
            print('Error!', install_error.decode())
    else:
        print('Closing....\nunsupported platform type!')
        sys.exit(1)
