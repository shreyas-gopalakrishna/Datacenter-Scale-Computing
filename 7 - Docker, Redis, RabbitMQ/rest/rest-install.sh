#!/bin/sh
#
# This is the script you need to provide to install the rest-server.py and start it running.
# It will be provided to the instance using redis-launch.sh
#

REST_SERVER=$(curl http://metadata/computeMetadata/v1/instance/attributes/rest-server -H "Metadata-Flavor: Google")

sudo apt-get update
sudo apt-get install -y python3 python3-pip git
git clone https://github.com/pallets/flask.git
cd flask/examples/tutorial
sudo python3 setup.py install
sudo pip3 install -e .

sudo pip3 install pillow
pip3 install jsonpickle
pip3 install numpy
pip3 install pika
pip3 install redis

cd
echo "$REST_SERVER" > rest-server.py
# python3 rest-server.py