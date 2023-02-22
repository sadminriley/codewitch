#!/usr/bin/env python3.11
import docker
import glob
import os
import uuid
import logging
import subprocess
from decouple import config
from git import Repo
from pathlib import Path


'''
 Check for choice of dockerhub, image registry, or git source for the app being built.
 This creates an infrastructure of choice(AWS,Azure,GCP,ETC) from the front-end with this script that runs anywhere(in a Docker container, of course!) on your infrastructure or a remote source, and runs using  mostly
 docker and a config file with decouple.
 This script MUST be run as root!


Must have .env file for python-decouple
APP_SOURCE=dockerhub,registry,git
HUB_IMAGE=someurl/repo
HUB_URL
GIT_URL=gitgud.com/baebaz.git
LANG=python, node, ruby, php
FLASK_USER=test
FLASK_PASS=supersecret
'''

# The None values for the decouple config .env were so vim/pycharm ignores warnings

# config file stuff


if config('GIT_URL') is not None:
    print('GIT_URL is %s' % config('GIT_URL'))
    GIT_URL = config('GIT_URL')


if config('HUB_IMAGE') is not None:
    print('GIT_URL not found in config file, using Docker...')
    HUB_IMAGE = config('HUB_IMAGE')


# Connect to the docker client

docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')


Logger = logging.getLogger(__name__)


    print('Log here to show container being pulled')


def run_docker(hub_image):
    docker_client.containers.run(hub_image)
    print('Some Logging stuff to show running containers')



# Create unique log id for log tags
unique_log_id = str(uuid.uuid4().int & (1 << 64) - 1)


def log_info(func_name, tags=None) -> None:
    Logger.info(func_name, tags)


def log_error(func_name, tags=None) -> None:
    Logger.error(func_name, tags)


def run_docker_detach(hub_image):
    container = docker_client.containers.run(hub_image, detach=True)
    container.logs()


# Kube functions
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


# Consume docker compose stack with kompose.io and run it on the desired platform

def docker_kompose(file_dir=os.getcwd(),
                   json_conversion=False,
                   helm=False,
                   repc=False,
                   repc_replicas=1,
                   daemonset=False,
                   statefulset=False):
    # Conversion types
    if bool(json_conversion):
        run_kompose_json(file_dir)
    elif bool(helm):
        run_kompose_helm(file_dir)
    elif bool(repc):
        run_kompose_repcontroller(file_dir, repc_replicas)
    elif bool(daemonset):
        run_kompose_daemonset(file_dir)
    elif bool(statefulset):
        run_kompose_statefulset(file_dir)
    else:
        run_kompose(file_dir)


# This returns a list of found files from the below provided file names

file_ext = ['docker-compose.yaml', 'docker-compose.yml']

file_names = [fn for fn in os.listdir(os.getcwd()) if any(fn.endswith(ext) for ext in file_ext)]


def get_kompose_files(file_names):
    for item in file_names:
        run_kompose(item)


def kubectl_apply():
    for file in glob.glob("*.yaml"):
        if file != 'docker-compose.yaml':
            subprocess.run([f"kubectl", "apply", "-f", file])


def parse_arguments():
    '''
    Parsing user arguments. Use -h to see commands. These will be passed to through script via Docker
    '''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kompose',
                        help='Convert docker-compose.yml to k8s configs in YAML',
                        action='store_true')
    parser.add_argument('--kompose-json',
                        help='Convert docker-compose.yml to k8s configs in JSON',
                        action='store_true')
    parser.add_argument('--kompose-helm',
                        help='Convert docker-compose.yml to k8s Helm chart',
                        action='store_true')
    parser.add_argument('--kompose-repc',
                        help='Convert docker-compose.yml to get k8s replication controller configs',
                        action='store_true')
    parser.add_argument('--kompose-daemonset',
                        help='Convert docker-compose.yml to get k8s daemonset',
                        action='store_true')
    parser.add_argument('--kompose-stateful',
                        help='Convert docker-compose.yml to get k8s statefulset',
                        action='store_true')


    args = parser.parse_args()
    return args






# Example
#docker_kompose() # Run the function to convert files for k8s
#kubectl_apply() # Apply the files

# docker_kompose(json_conversion=True) will return .json files
# docker_kompose(helm=True) will generate a helm chart
