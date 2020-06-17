#!/bin/sh
#
# This is the script you need to provide to install the rest-server.py and start it running.
# It will be provided to the instance using redis-launch.sh
#
sudo apt-get update

# Install prerequisites
sudo apt-get install -y libopencv-dev libtesseract-dev git cmake build-essential libleptonica-dev
sudo apt-get install -y liblog4cplus-dev libcurl3-dev

# If using the daemon, install beanstalkd
sudo apt-get install -y beanstalkd

cd 
# Clone the latest code from GitHub
sudo git clone https://github.com/openalpr/openalpr.git

# Setup the build directory
cd openalpr/src
sudo mkdir build
cd build

# setup the compile environment
sudo cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..

# compile the library
sudo make

# Install the binaries/libraries to your local system (prefix is /usr)
sudo make install

sudo add-apt-repository ppa:alex-p/tesseract-ocr -y
sudo apt-get update -y

sudo apt-get purge libtesseract-dev
sudo apt-get install -y libtesseract-dev

sudo apt-get install -y python3-pip  

cd ../bindings/python/
sudo python3 setup.py install

#
# Install other packages as needed
#
apt-get install -y python3 python3-pika python3-pillow python3-openalpr python3-redis
