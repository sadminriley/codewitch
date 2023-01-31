#!/usr/bin/env python3.11
# Kompose related functions
import os
import lsb_release
import platform
import subprocess
import sys


distro_info = lsb_release.get_distro_information()


KOMPOSE_PATH = "/usr/local/bin/kompose"


# Check for existing kompose install, installs it otherwise
def check_kompose():
    if not os.path.exists(KOMPOSE_PATH):
        install_kompose()
    else:
        print("\n %s already found. Not installing. \n" % KOMPOSE_PATH)


def install_kompose():
    if 'Ubuntu' in distro_info['DESCRIPTION']:
        install_process = subprocess.Popen("./install_kompose_deb.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Installs 'Most' Linux distros
        success, install_error = install_process.communicate()
        if not install_error:
            print('Install complete', success.decode())
        else:
            print('Error!', install_error.decode())
    elif 'Fedora' in distro_info['DESCRIPTION']:
        install_process = subprocess.Popen("./install_kompose_redhat.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # installs via DNF pkg manager
        success, install_error = install_process.communicate()
        if not install_error:
            print('Install complete', success.decode())
        else:
            print('Error!', install_error.decode())
    else:
        print('Closing....\nunsupported platform type!')
        sys.exit(1)



def run_kompose(dir_name=os.getcwd()):
    # Log the run command output
    try:
        subprocess.run(["kompose", "convert"])
    except subprocess.CalledProcessError as e:
        print(e.output)


def run_kompose_json(dir_name=os.getcwd()):
    # Log the run command output
    # Generate JSON from yml
    try:
        subprocess.run(["kompose", "convert", "-j"])
    except subprocess.CalledProcessError as e:
        print(e.output)


def run_kompose_helm(dir_name=os.getcwd()):
    # Log the run command output
    # Generate Helm chart
    try:
        subprocess.run(["kompose", "convert", "-c"])
    except subprocess.CalledProcessError as e:
        print(e.output)


# Convert only replicationController objects with optional replicaset number. Defaults to 1
def run_kompose_repcontroller(dir_name=os.getcwd(), replicas=1):
    # Log the run command output
    try:
        cmd = f"kompose convert --controller replicationController --replicas {replicas}"
        subprocess.call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)



def run_kompose_daemonset(dir_name=os.getcwd()):
    # Log the run command output
    # Generate *-daemonset.yaml files
    try:
        subprocess.run(["kompose", "convert", "--controller", "daemonSet"])
    except subprocess.CalledProcessError as e:
        print(e.output)


def run_kompose_statefulset(dir_name=os.getcwd()):
    # Log the run command output
    # Generate *-statefulset.yaml files
    try:
        subprocess.run(["kompose", "convert", "--controller", "statefulSet"])
    except subprocess.CalledProcessError as e:
        print(e.output)
