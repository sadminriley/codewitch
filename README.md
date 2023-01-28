# CodeWitch Prototype
This is the wip for this idea. I wanted to bring together numerous open source tools to deploy code and manage infrastructure better.
Very few functions work as of right now.

The first thing to fully work will be converting a singular docker-compose.yaml file to kubernetes configs
and successfully creating the surrounding infrastructure for kubernetes to deploy the docker image from applied config files.


## What is CodeWitch?

CodeWitch aims to create infrastructure from Docker, Docker Compose, and Git sources. CodeWitch can run a variety of different types of
coding languages, and is compatible with AWS/GCP/Azure.


It will eventually do many other things like create infrastructure based on resource crawling, collect metrics, and report data.

All functions will be tied into a lightweight, flexible front-end. It will probably leverage Terraform via Python to create infrastructures, eventually.
