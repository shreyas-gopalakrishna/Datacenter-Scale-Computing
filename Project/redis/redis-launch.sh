#!/bin/sh
docker pull redis
docker tag redis gcr.io/dcsc-3/redis
docker push gcr.io/dcsc-3/redis

kubectl create deployment redis --image=gcr.io/dcsc-3/redis
kubectl expose deployment redis --type=LoadBalancer --port 6379