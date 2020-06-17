#!/bin/sh
#
# This is the script you need to provide to install redis and start it running.
# It will be provided to the instance using redis-launch.sh
#
sudo apt update
sudo apt install -y redis-server
sudo echo "bind 0.0.0.0 ::1" >> /etc/redis/redis.conf
sudo systemctl restart redis-server