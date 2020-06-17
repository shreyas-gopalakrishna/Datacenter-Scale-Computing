#!/bin/sh
docker pull rabbitmq
docker tag rabbitmq gcr.io/dcsc-3/rabbitmq
docker push gcr.io/dcsc-3/rabbitmq

kubectl create deployment rabbitmq --image=gcr.io/dcsc-3/rabbitmq
kubectl expose deployment rabbitmq --type=LoadBalancer --port 5672
