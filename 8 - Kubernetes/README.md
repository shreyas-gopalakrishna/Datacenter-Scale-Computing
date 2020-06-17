# lab8-alpr-kubernetes
Automatic license plate recognition service implemented using kubernetes.

## Overview
In this lab, you're going to create a kubernetes cluster that provides a REST API for scanning images that contain geotagged license plates and records them in a database.

You may [want to bookmark this kubernetes "cheat sheet"](https://kubernetes.io/docs/reference/kubectl/cheatsheet/).

You should also have completed the QwikLabs tutorials on using Docker and Kubernetes. You can get a quick refresher by [referring to this tutorial on deploying a simple "hello world" application](https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app). That example (and the QwikLab tutorials) shows you how to construct a simple Dockerfile, build a Docker image, push it to the Google registry and then deploy it on Kubernetes. You can either use the Google cloud shell to do your work or install Docker on your laptop.

You will deploy containers providing the following services.
+ rest - the REST frontend will accept images for analysis and handle queries concerning specific license plates and geo-coordinates. The REST worker will queue tasks to workers using `rabbitmq` messages. Full details are provided in `rest/README-rest.md`
+ worker - Worker nodes will receive work requests to analyze images. If those images contain both a geo-tagged image and a vehicle with a license plate that can be scanned, the information is entered into the REDIS database. Full details are provided in worker/README-worker.md
+ rabbitmq - One node, which should be named `rabbitmq` should act as the rabbit-mq broker. Full details are provided in rabbitmq/README-rabbitmq.md . Feel free to build your own container image [or use the one provided by the Rabbitmq developers](https://hub.docker.com/_/rabbitmq).
+ redis - One node, which should be named 'redis' should provide the redis database server. Full details are provided in redis/README-redis.md . Feel free to build your own container image [or use the one provided by the Redis developers](https://hub.docker.com/_/redis).

The worker will use the [open source automatic license plate reader](https://github.com/openalpr/openalpr) software. This is an open-source component of [a more comprehensive commercial offering](https://openalpr.com). One of the commercial components includes a web service similar to what we're building.

You will need to create a Kubernetes cluster to run your code. This is done by issuing the following `gcloud` commands:
```
gcloud config set compute/zone us-west1-b
gcloud container clusters create --preemptible mykube
```
By default, this will create a 3-node cluster of `n1-standard-1` nodes. The `-premptible` flag drops the price, but your cluster will be removed within 24 hours and may be deleted at any moment. Generally, this isn't a problem, but you can omit it if you're worried.

## Suggested Steps

You should first deploy the `rabbitmq` and `redis` deployments because they're easy, particularly if you deploy the versions provided by the developers. For each of those, you'll need to specify a deployment and then create a Service for that deployment. Following that, you should construct the `rest` server because you can use that to test your `redis` database connection as well as connections to `rabbitmq` and your debugging interface. Lastly, start on the `worker`.

Although not explicitly required, you should create a simple python program that connects to the debugging topic exchange as described in `rabbitmq`. You can use that to subscribe to any informational or debug messages to understand what's going on. It's useful to deploy that service as a "logs" pod (or deployment) so you can monitor the output using `kubectl logs logs-<unique id for pod>`

You should use version numbers for your container images. If you're in a edit/deploy/debug cycle, your normal process to deploy new code will be to push a new container image and then delete the existing pod (rest or worker). At that point, the deployment will create a new pod. If you're using version numbers, you'll be able to insure that you're running the most recent code.

Each subdirectory contains directions in the appropriate README file. The `images` directory contains test images.
+ beetle.jpg is not geotagged and has one visible license plate (309-OJN)
+ car.jpg is not geotagged but has one visible license (CZTHEDA)
+ geotagged.jpg is geotagged but has no cars
+ the-meat-car.jpg is geotagged and has one visible license (789-SJL but reported as 7B9SJLD)

The `plate1.png` image is a PNG image -- you can use this to test what happens when non-jpg files are submitted.
