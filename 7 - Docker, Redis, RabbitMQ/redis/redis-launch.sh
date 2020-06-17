#!/bin/sh
#
# This is the script you need to provide to launch a redis instance
# and cause it to run the redis-install.sh script
#
gcloud compute instances create redis \
--image-family ubuntu-1804-lts \
--image-project gce-uefi-images \
--zone us-west1-b \
--network-interface=no-address \
--metadata-from-file=startup-script=redis-install.sh \
--tags default-allow-internal