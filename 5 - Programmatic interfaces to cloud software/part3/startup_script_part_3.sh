#!/bin/bash

# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START startup_script]
apt-get update

# Use the metadata server to get the configuration specified during
# instance creation. Read more about metadata here:
# https://cloud.google.com/compute/docs/metadata#querying
SERVICE_ACCOUNT=$(curl http://metadata/computeMetadata/v1/instance/attributes/serviceAccount -H "Metadata-Flavor: Google")
INSTANCE_SCRIPT=$(curl http://metadata/computeMetadata/v1/instance/attributes/instanceScript -H "Metadata-Flavor: Google")
STARTUP_SCRIPT=$(curl http://metadata/computeMetadata/v1/instance/attributes/startupScriptInstance -H "Metadata-Flavor: Google")


mkdir lab5-part3
cd lab5-part3
echo "$SERVICE_ACCOUNT" > service-credentials.json
echo "$INSTANCE_SCRIPT" > create_instance.py
echo "$STARTUP_SCRIPT" > startup-script.sh

# Git clone and install Flask
sudo apt-get update
sudo apt-get install -y python3 python3-pip git

sudo pip3 install --upgrade google-api-python-client

sudo python3 create_instance.py dcsc-2 dcsc-bucket --zone us-west1-b --name dcsc-instance-part-3-vm2

# [END startup_script]
