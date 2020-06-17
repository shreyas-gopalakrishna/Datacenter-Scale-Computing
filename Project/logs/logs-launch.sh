#!/bin/sh
docker build -t logs .
docker tag logs gcr.io/dcsc-3/logs
docker push gcr.io/dcsc-3/logs

kubectl create deployment logs --image=gcr.io/dcsc-3/logs
