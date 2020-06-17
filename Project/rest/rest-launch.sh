#!/bin/sh
docker build -t rest .
docker tag rest gcr.io/dcsc-3/rest
docker push gcr.io/dcsc-3/rest

kubectl create deployment rest --image=gcr.io/dcsc-3/rest
kubectl expose deployment rest --type=LoadBalancer --port 5000
