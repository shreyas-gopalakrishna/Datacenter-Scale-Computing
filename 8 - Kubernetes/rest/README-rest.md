# REST API and interface

You must create a script `rest-launch.sh` that creates the a container image from a Dockerfile, pushes it to the `gcr.io` repository, creates a deployment using that image and creates an external endpoint using a load balancer or ingress node. This container is the only container in your cluster that should have an external endpoint.

You must provide a `rest-server.py` that implements a Flask server that responds to the endpoints below. and package that into a web server. You'll also need to provide a `rest-client.py` that can send images to the `rest-server.py`. Other endpoints can be tested using `curl`.

+ http://<ip>/image/[filename] [PUT] - scan the picture passed as the content of the request and with the specified filename. Compute the MD5 of the contents and send the MD5 and image to a worker using the `toWorker` rabbitmq exchange. The filename should be added to the Redis database as described in the worker documentation; this can be done by the Rest server or the worker. The response of this API should be a JSON document containing a single field `hash` that is the md5 hash used to identify the provided image. For example:
```
  { 'hash' : "abcedef...128" }
```
+ http://<ip>/hash/[checksum] [GET] -- using the checksum, return a list of the license plates and geotagged information associated with the picture for which that is the checksum. If the image had no geotags or license plates, an empty list is returned.
+ http://<ip>/license/[licence] [GET] -- using the provided license string, return a list of the checksums that contain this license plate. If the license doesn't exist in any processed image, an empty list is returned.

Using the /license/ endpoint, you can retrieve the image checksums for the license and then get the details about distinct images using the /hash/ endpoint.

You will need two RabbitMQ exchanges.
+ A `topic` exchange called `logs` used for debugging and logging output
+ A `direct` exchange called `toWorker` used by the REST API to send images to the worker

You should use the topic exchange for debug messages with the topics `[hostname].rest.debug` and `[hostname].rest.info`, substituting the proper hostname. You can include whatever debugging information you want, but you must include a message for each attempted API call and the outcome of that call (successful, etc).

You may find it useful to create a `logs` container and deployment that listen to the logs and dumps them out to `stderr` so you can examine them using `kubectl logs..`.

When installing the `pika` library used to communicate with `rabbitmq`, you should use the `pip` or `pip3` command to install the packages. E.g.
```
sudo pip3 install --upgrade pika
```