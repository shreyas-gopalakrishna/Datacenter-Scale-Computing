#!/bin/sh
#
# This is the script you need to provide to launch a redis instance
# and cause it to run the redis-install.sh script
#
gcloud compute instances create add-worker \
--image worker-image \
--zone us-west1-b \
--network-interface=no-address \
--metadata-from-file=startup-script=add-worker-install.sh,worker=worker.py \
--tags default-allow-internal