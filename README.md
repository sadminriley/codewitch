# CodeWitch + Aphrodite Prototype


[![CircleCI](https://dl.circleci.com/status-badge/img/gh/sadminriley/codewitch/tree/trunk.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/sadminriley/codewitch/tree/trunk)


This is the wip for this idea. I wanted to bring together numerous open source tools to deploy code and manage infrastructure better.
Very few functions work as of right now.

The first thing to fully work will be converting a singular docker-compose.yaml file to kubernetes configs
and successfully creating the surrounding infrastructure for kubernetes to deploy the docker image from applied config files. This works now, at a very
rudimentary level.

Something I often ask and wonder - what if we could just make production ready stacks from docker-compose or Dockerfile's with an open-source tool? It could also create infrastructures, template Docker related files, and perhaps Cloudformation amongst Terraform.

I've noticed many, many SaaS companies charging for similar tools by adding a nice GUI on top of it.


## What is CodeWitch?

CodeWitch aims to create infrastructure from Docker, Docker Compose, and Git sources. CodeWitch can run a variety of different types of
coding languages, and is compatible with AWS/GCP/Azure.


## What is Aphrodite?

First, this was going to just be a very simple tool. I wanted it to have the ability to create production ready Kuberentes clusters from Docker files,
especially compose stacks. That functionaility will be broken into it's own repo soon.


Meet Aphrodite! Aphrodite has more of a focus on things like -
Building autuomated infrastructure environments, migrations, and metrics/data reoprting.



## TODO
#### Komposer.py
[*] Check for existing kompose install and get komposer.py functions working
[]  Implement OpenShift support
[]  Fix PVC issues
[]  Better image pulls
[]  Kompose up support

#### Dockerops.py
[] Add argparse accordingly for Dockerization.

#### Dockerfile
[*] Create Dockerfile and run kompose conversions successfully


#### Everything else
[] A whole lot of things.



#### Kompose functions from the sample docker-compose.yaml in lib applied to minikube -

```
python3.11 dockerops.py
GIT_URL is bar
GIT_URL not found in config file, using Docker...
INFO Kubernetes file "frontend-tcp-service.yaml" created
INFO Kubernetes file "redis-master-service.yaml" created
INFO Kubernetes file "redis-slave-service.yaml" created
INFO Kubernetes file "frontend-deployment.yaml" created
INFO Kubernetes file "redis-master-deployment.yaml" created
INFO Kubernetes file "redis-slave-deployment.yaml" created
deployment.apps/redis-slave created
lservice/redis-slave configured
^Hdeployment.apps/frontend created
deployment.apps/redis-master created
service/frontend-tcp configured
service/redis-master configured

```

You should be able to see the pods running now


```
kubectl get po
NAME                           READY   STATUS    RESTARTS   AGE
frontend-59fcdb96b7-fc7dx      1/1     Running   0          8s
redis-master-bb667cb7d-kb4lj   1/1     Running   0          8s
redis-slave-5bff569f56-zf4hg   1/1     Running   0          8s
```


#### Env file for decouple config


Warning: Plain .env examples are shown in this repo. You'd want to gitignore .env for development, and pull sensitive values from elsewhere for it.

```
APP_SOURCE=dockerhub
HUB_IMAGE=redis
HUB_URL=foo
GIT_URL=bar
LOG_STREAM=default
FLASK_USER=test
FLASK_PASS=supersecret
SECRET_KEY=

```

The flask_upload.py will not work without the FLASK_USER and FLASK_PASS set. SECRET_KEY will be created on run if None is passed.


### Flask_upload.py


This allows you to upload a docker-compose file with either .yml or .yaml. Launch the flask_upload.py and upload your file as such -

<img src="https://user-images.githubusercontent.com/25120457/220446355-cbcaecb2-e65a-416d-8fd9-99aa286401a3.png" width="90%"></img> <img src="https://user-images.githubusercontent.com/25120457/220446436-55c73644-1135-4745-95e1-9811c5f5cfe2.png" width="90%"></img>

The comic sans is just for fun :) , of course.


The flask routes now apply kubefiles via the following -
```
curl -X GET 127.0.0.1:5000/kube/apply                                                                            [19:31:55]
{
  "success": true
}
```

Now, you should see the app do this

```
deployment.apps/redis-slave created
service/redis-slave configured
deployment.apps/frontend created
deployment.apps/redis-master created
service/frontend-tcp configured
service/redis-master configured
127.0.0.1 - - [06/Mar/2023 19:33:39] "GET /kube/apply HTTP/1.1" 200 -
```
