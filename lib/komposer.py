#!/usr/bin/env python3.11
# Kompose related functions
import os
import platform
import subprocess


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



def run_kompose(dir_name=os.getcwd()):
    # Log the run command output
    try:
        subprocess.run(["kompose", "konvert"])
    except subprocess.CalledProcessError as e:
        print(e.output)


def run_kompose_json(dir_name=os.getcwd()):
    # Log the run command output
    # Generate JSON from yml
    try:
        subprocess.run(["kompose", "konvert", "-j"])
    except subprocess.CalledProcessError as e:
        print(e.output)


def run_kompose_helm(dir_name=os.getcwd()):
    # Log the run command output
    # Generate Helm chart
    try:
        subprocess.run(["kompose", "konvert", "-c"])
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

