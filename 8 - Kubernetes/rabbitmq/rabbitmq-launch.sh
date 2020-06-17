#!/bin/sh
#
# This is the script you need to provide to launch a rabbitmq instance
# service
#
docker pull rabbitmq
docker tag rabbitmq gcr.io/dcsc-2/rabbitmq:0.1
docker push gcr.io/dcsc-2/rabbitmq:0.1

kubectl create deployment rabbitmq --image=gcr.io/dcsc-2/rabbitmq:0.1
kubectl expose deployment rabbitmq --type=ClusterIP --port 5672