#!/bin/sh
#
# This is the script you need to provide to install rabbitmq and start it running.
# It will be provided to the instance using rabbitmq-launch.sh
#

sudo apt-get update
wget https://packages.erlang-solutions.com/erlang/debian/pool/esl-erlang_22.1.6-1~ubuntu~bionic_amd64.deb
sudo apt-get install -y libwxbase3.0-0v5 libwxgtk3.0-0v5 libsctp1
sudo dpkg -i esl-erlang_22.1.6-1~ubuntu~bionic_amd64.deb
sudo apt-get install -f
wget -O- https://dl.bintray.com/rabbitmq/Keys/rabbitmq-release-signing-key.asc | sudo apt-key add -
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
echo "deb https://dl.bintray.com/rabbitmq/debian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/rabbitmq.list
sudo apt update
sudo apt -y install rabbitmq-server
sudo bash -c "echo loopback_users=none > /etc/rabbitmq/rabbitmq.conf"
sudo systemctl restart rabbitmq-server