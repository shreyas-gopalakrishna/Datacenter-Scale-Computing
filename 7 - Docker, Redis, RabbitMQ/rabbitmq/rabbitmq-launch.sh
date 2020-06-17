#!/bin/sh
#
# This is the script you need to provide to launch a rabbitmq instance
# and cause it to run the rabbitmq-install.sh script
#
gcloud compute instances create rabbitmq \
--image-family ubuntu-1804-lts \
--image-project gce-uefi-images \
--zone us-west1-b \
--network-interface=no-address \
--metadata-from-file=startup-script=rabbitmq-install.sh \
--tags default-allow-internal