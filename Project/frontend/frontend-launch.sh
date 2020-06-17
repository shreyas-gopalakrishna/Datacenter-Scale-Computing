#!/bin/sh
docker build -t frontend .
docker tag frontend gcr.io/dcsc-3/frontend
docker push gcr.io/dcsc-3/frontend

kubectl create deployment frontend --image=gcr.io/dcsc-3/frontend
kubectl expose deployment frontend --type=LoadBalancer --port 80