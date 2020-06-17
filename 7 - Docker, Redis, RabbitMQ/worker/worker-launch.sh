#!/bin/sh
#
# This is the script you need to provide to launch a worker instance
# and cause it to run the worker-install.sh script
#
gcloud compute instances create worker2 \
--image-family ubuntu-1804-lts \
--image-project ubuntu-os-cloud \
--zone us-west1-b \
--network-interface=no-address \
--metadata-from-file=startup-script=worker-install.sh \
--tags default-allow-internal