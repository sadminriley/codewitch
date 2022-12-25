#!/usr/bin/env python3.11
import docker
import os
from git import Repo
from decouple import config


# Check for choice of dockerhub, image registry, or git source for the app being built.
# This creates an infrastructure of their choice(AWS,Azure,GCP,ETC) from the front-end with this script that runs anywhere(in a Docker container, of course!) on THEIR infra or ours, and runs using  mostly
# docker and a config file with decouple.

'''
Must have .env file for python-decouple
APP_SOURCE=dockerhub,registry,git
HUB_IMAGE=someurl/repo
HUB_URL
GIT_URL=gitgud.com/baebaz.git
LANG=python, node, ruby, php


'''

# The None values for the decouple config .env were so pycharm ignores warnings

# config file stuff


if config('GIT_URL') is not None:
    print('GIT_URL is %s' % config('GIT_URL'))
    GIT_URL = config('GIT_URL')



if config('HUB_IMAGE') is not None:
    print('GIT_URL not found in config file, using Docker...')
    HUB_IMAGE = config('HUB_IMAGE')




'''
if config('APP_SOURCE') == 'dockerhub':
    HUB_URL = config('HUB_URL') # Docker hub image pull url
elif config('APP_SOURCE') == 'registry':
    HUB_URL = config('HUB_URL')
else:
    GIT_URL = config('GIT_URL')
'''
# Connect to the docker client

client = docker.DockerClient(base_url='unix://var/run/docker.sock')



def clone_git(git_url):
    Repo.clone_from(repo, repo_dir=os.getcwd())



def pull_docker(hub_image, tag=None):
    client.images.pull(hub_image, tag) # Pull the docker image
    print('Log here to show container being pulled')




# keeping this same function for organizational purposes
def pull_registry(hub_image):
    client.images.pull(hub_image)  # Pull the docker image

    print('Log here to show container being pulled')


def run_docker(hub_image):
    client.containers.run(hub_image)
    print('Some Logging stuff to show running containers')


def run_docker_detach(hub_image):
    client.containers.run(hub_image, detach=True)
    print('Some Logging stuff to show detached containers')




## Consume docker compose stack with kompose.io and run it on the desired platform

def docker_kompose(composefile):
    Komposer(composefile)





pull_docker(HUB_IMAGE)

run_docker(HUB_IMAGE)

