# ALPR Worker

The steps you need to take:
+ Create a worker image that can execute OpenALPR, run RabbitMQ clients and has access to a remote Redis database
+ Develop a Python program that listens to the `toWorkers` RabbitMQ exchange, receives a message, check for geotags and if found, scans for a license plate.
+ Create a shell script or python program that will automatically launch another worker.

## Creating a worker image
You should first create a "worker image" and then use that to create multiple worker instances.

You can either use a Python program to create the worker image, or a series of `gcloud` commands. In particular, you may want to use [`gcloud compute instances create](https://cloud.google.com/sdk/gcloud/reference/compute/instances/create) with the `--metadata-from-file` option to specify the startup script that will install software.

You'll be provided with a `build-worker-src.sh` script that installs the OpenALPR software from source. Although Ubuntu 18.04 has an OpenALPR package, it doesn't work. You can use the packaged version if you use Ubuntu 19.10 and script `build-worker-u19.10.sh` which installs the appropriate package and fixes an error in the provided installation.

You can install your Python program by providing it via the `--metadata-from-file` option and copying it to a location you specify or whatever method you prefer. Your final image file should have all software needed installed to reduce the time needed to launch a new worker.

Once you have your worker configured, [create an image using the gcloud command line or a program](https://cloud.google.com/sdk/gcloud/reference/compute/images/create). You'll use that to spin up other workers.

File `worker-install.sh` should contain the configuration and code you choose to use in building your worker (probably copied from `build-worker-u19.10.sh` or `build-worker-src.sh`). File `worker-launch.sh` should launch an instance that you can then shutdown and use to create an image. File `worker-addworker.sh` should start up a new worker using the image you constructed.

## Program to process images

You will need two RabbitMQ exchanges.
+ A `topic` exchange called `logs` used for debugging and logging output
+ A `direct` exchange called `toWorker` used by the REST API to send images to the worker

You can use whatever method you like to get data from the REST API to the worker. For example, you could create a Python datatype including the image, then `pickle` the image and send it via RabbitMQ. Or, you could store the image in Google object storage and send a smaller message.

Upon receiving the message, you should first determine if the image contains geotagged information. The sample program `provided-GetLatLon.py` shows you how to extract the latitude and longitude from a photo. See the description of the images to test your code.  Other image formats, such as `png` don't support the extended headers we're looking for; however, your solution should be robust to being handed bad image files.

If the image is geotagged, you should then look for a license plate. You can use the [python API for this](https://pypi.org/project/openalpr/) or use the command line. The file `provided-getAlpr.py` shows an example of using the python API to scan an image and pull the most likely plate.

Following this, if the image is both geotagged and has a license plate, you will update the Redis database with the results. Redis is a Key-Value store that has simple Get/Put methods and also has an internal "list" datatype. You can read more about [the Python interface](https://pypi.org/project/redis/). Redis supports a number of datatypes including lists and sets. In many cases, the set data type will be the most appropriate because we only want a single instance of a data item associated with a key.

We will be using 3 Redis databases. Redis uses numbers for database names, and we'll be using 1, 2 & 3. The '0' database is the default. The three different key-value stores have the following composition.
```
##
## This database has key "md5" (of a photo) and value(s)
## of the licenses and lat/lon found in the photo. The values can
## be stored as a string -- you can assume that ':' doesn't appear
## in license plates e.g. "license:confidence:lat:lon" is a possible encoding.
## If multiple licenses are found (e.g. with difference confidence) you should
## add all of them to the database.
## 
redisByChecksum = redis.Redis(host=redisHost, db=1)
## 
## This database has key "filename" (of a photo) and
## values the MD5's of photos submitted with that name.
## Note that an image may be submitted under multiple names
## and images with the same name may have different MD5's.
##                                                                              
redisByName = redis.Redis(host=redisHost, db=2)
##                                                                              
## This database has key "license" and value(s)
## the md5 hashes in which the license is stored.
##                                                                              
redisMD5ByLicense = redis.Redis(host=redisHost, db=3)
```
Redis also supports [limited geo-spatial indexes](https://www.infoworld.com/article/3128306/build-geospatial-apps-with-redis.html) but you don't need to use those unless you want to extend the homework.

Once the database has been updated or when you determine there is no geotagged information and/or you can't get a license plate, you should then `acknowledge` the RabbitMQ message. You should only acknowledge it after you've processed it.

At each step of your processing, you may want to log debug information using the `topic` queue and `[hostname].worker.debug`. When you've added the data to the database, you *must* log that as `[hostname].worker.info`, substituting the proper worker name.

## Create shell script to launch workers

You should create a shell script `worker-addworker.sh` (using the `gcloud` commands) or a python program to launch a new worker. That script must also start the worker script in the image. Make sure that your instance does not have an external IP address using the `--network-interface=no-address` flag if using the `gcloud` command interface or similar method if using Python.

You should verify (using the rabbitmq `topic` queue) that you can process images correctly and enter them in the database.

You should then verify that you can launch a new worker and it too will process images. Lastly, you should verify that if you destroy a worker, the remaining workers can process the images.

You will have to demonstrate all of these steps in your grading interview.