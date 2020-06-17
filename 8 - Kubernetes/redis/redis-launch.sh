#!/bin/sh
#
# This is the script you need to provide to launch a redis instance
# and and service
#
docker pull redis
docker tag redis gcr.io/dcsc-2/redis:0.1
docker push gcr.io/dcsc-2/redis:0.1

kubectl create deployment redis --image=gcr.io/dcsc-2/redis:0.1
kubectl expose deployment redis --type=ClusterIP --port 6379
