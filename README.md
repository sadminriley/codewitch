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


## TODO
#### Komposer.py
[*] Check for existing kompose install and get komposer.py functions working

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






