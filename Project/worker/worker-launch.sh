#!/bin/sh
docker build -t worker .
docker tag worker gcr.io/dcsc-3/worker
docker push gcr.io/dcsc-3/worker

kubectl create deployment worker --image=gcr.io/dcsc-3/worker
