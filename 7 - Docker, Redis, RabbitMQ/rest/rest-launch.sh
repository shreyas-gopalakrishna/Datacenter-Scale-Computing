#!/bin/sh
#
# This is the script you need to provide to launch a redis instance
# and cause it to run the rest-install.sh script
#
gcloud compute instances create rest \
--image-family ubuntu-1804-lts \
--image-project gce-uefi-images \
--zone us-west1-b \
--metadata-from-file=startup-script=rest-install.sh,rest-server=rest-server.py